import os
import json
import tempfile
import zipfile

import geopandas as gpd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from shapely import wkt
from rest_framework import viewsets
from .models import Pidana
from .serializers import *

# ==============================
# Helper: load layer from DB
# ==============================
def load_layer_from_db(table):
    geom_col = "ogr_geometry"
    # print(table )
    with connection.cursor() as cursor:
        # print(cursor)
        cursor.execute(f"""
            SELECT ogr_geometry.STAsText() AS wkt_geom FROM \"{table}\"
        """)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    records = []

    for row in rows:
        rec = dict(zip(columns, row))
        geom_wkt = rec.pop("wkt_geom", None)
        rec["geometry"] = wkt.loads(geom_wkt) if geom_wkt else None
        records.append(rec)

    gdf = gpd.GeoDataFrame(records, geometry="geometry", crs="EPSG:4326")
    # print(records)
    return gdf

# ==============================
# Helper: parse uploaded file
# ==============================
def read_uploaded_file(uploaded_file, tmpdir):
    upload_path = os.path.join(tmpdir, uploaded_file.name)

    with open(upload_path, "wb+") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    if zipfile.is_zipfile(upload_path):
        with zipfile.ZipFile(upload_path, "r") as z:
            z.extractall(tmpdir)

        for f in os.listdir(tmpdir):
            if f.lower().endswith((".shp", ".geojson", ".json", ".kml", ".gpkg")):
                return os.path.join(tmpdir, f)
    else:
        return upload_path

    return None

# ==============================
# MAIN API
# ==============================
@csrf_exempt
def api_analyze(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST supported"}, status=405)

    try:
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Save & read input file
        with tempfile.TemporaryDirectory() as tmpdir:
            spatial_path = read_uploaded_file(uploaded_file, tmpdir)

            if not spatial_path:
                return JsonResponse({"error": "Unsupported spatial file"}, status=400)

            gdf_input = gpd.read_file(spatial_path)

        # CRS standardization
        gdf_input = gdf_input.to_crs("EPSG:32751")

        # ==============================
        # Load layers from DB
        # ==============================
        layers = {
            "APL": load_layer_from_db("apl"),
            "HGB": load_layer_from_db("hgb"),
            "IPPKH": load_layer_from_db("ippkh"),
            "IUPK": load_layer_from_db("iupk"),
            "KKPR": load_layer_from_db("kkpr"),
            "Kawasan Hutan": load_layer_from_db("kawasan hutan"),
            "Lahan Bebas": load_layer_from_db("lahan_bebas"),
        }

        results = []
        geojson_layers = {}

        # ==============================
        # Spatial intersect
        # ==============================
        for name, gdf in layers.items():
            gdf = gdf.to_crs("EPSG:32751")

            clipped = gpd.overlay(gdf, gdf_input, how="intersection")

            if clipped.empty:
                area_m2 = 0
                geojson_layers[name] = None
            else:
                clipped["area_m2"] = clipped.geometry.area
                area_m2 = clipped["area_m2"].sum()

                geojson_layers[name] = json.loads(
                    clipped.to_crs("EPSG:4326").to_json()
                )

            results.append({
                "layer": name,
                "jumlah_fitur": len(clipped),
                "luas_m2": round(area_m2, 2),
                "luas_ha": round(area_m2 / 10000, 4)
            })

        # Input outline (user uploaded geometry)
        input_geojson = json.loads(gdf_input.to_crs("EPSG:4326").to_json())

        return JsonResponse({
            "input": input_geojson,
            "layers": geojson_layers,
            "stats": results
        }, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def tes():
    return JsonResponse({"mesage":"masuk bro"})


# class PidanaViewSet(viewsets.ModelViewSet):
#     queryset = Pidana.objects.all()
#     serializer_class = PidanaSerializer
# class ClaimViewSet(viewsets.ModelViewSet):
#     queryset = Claim.objects.all()
#     serializer_class = ClaimSerializer

def generate_viewset(model_name):
    model = apps.get_model('valemis', model_name)
    serializer = generate_serializer(model_name)

    class AutoViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer

    return AutoViewSet
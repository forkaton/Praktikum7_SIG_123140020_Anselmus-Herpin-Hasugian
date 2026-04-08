from fastapi import FastAPI, HTTPException, Query
import json
from contextlib import asynccontextmanager
import asyncpg # <-- Tambahan baru: kita panggil library asyncpg ke sini
from database import create_pool
from models import FasilitasCreate

# Inisialisasi pool koneksi dengan "Type Hinting" agar Pylance mengerti
pool: asyncpg.Pool | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await create_pool()
    yield
    if pool:
        await pool.close()

app = FastAPI(
    title="SIG API - Anselmus Herpin Hasugian",
    description="REST API untuk akses data spasial PostGIS Praktikum 7",
    lifespan=lifespan
)

# 1. Endpoint GET ALL (Mengambil semua data)
@app.get("/api/fasilitas", tags=["Fasilitas"])
async def get_all_fasilitas():
    if pool is None: # Pengecekan keamanan untuk Pylance
        raise HTTPException(status_code=500, detail="Database belum siap")
        
    async with pool.acquire() as connection:
        query = "SELECT id, nama, ST_X(geom) as longitude, ST_Y(geom) as latitude FROM fasilitas_publik"
        records = await connection.fetch(query)
        return [dict(record) for record in records]

# 2. Endpoint GET BY ID (Mengambil data spesifik)
@app.get("/api/fasilitas/{id}", tags=["Fasilitas"])
async def get_fasilitas_by_id(id: int):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database belum siap")
        
    async with pool.acquire() as connection:
        query = "SELECT id, nama, ST_X(geom) as longitude, ST_Y(geom) as latitude FROM fasilitas_publik WHERE id=$1"
        record = await connection.fetchrow(query, id)
        if not record:
            raise HTTPException(status_code=404, detail="Data tidak ditemukan")
        return dict(record)

# 3. Endpoint GET GEOJSON (Format standar peta)
@app.get("/api/geojson/fasilitas", tags=["Spasial"])
async def get_fasilitas_geojson():
    if pool is None:
        raise HTTPException(status_code=500, detail="Database belum siap")
        
    async with pool.acquire() as connection:
        query = """
        SELECT jsonb_build_object(
            'type', 'FeatureCollection',
            'features', jsonb_agg(ST_AsGeoJSON(t.*)::json)
        )
        FROM (SELECT id, nama, geom FROM fasilitas_publik) as t;
        """
        record = await connection.fetchval(query)
        if record:
            return json.loads(record)
        return {"type": "FeatureCollection", "features": []}

# 4. Endpoint GET NEARBY (Query Spasial)
@app.get("/api/spasial/nearby", tags=["Spasial"])
async def get_nearby_fasilitas(
    lon: float = Query(..., description="Longitude titik pusat"), 
    lat: float = Query(..., description="Latitude titik pusat"), 
    radius: float = Query(1000, description="Radius dalam meter")
):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database belum siap")
        
    async with pool.acquire() as connection:
        query = """
        SELECT id, nama, ST_X(geom) as longitude, ST_Y(geom) as latitude
        FROM fasilitas_publik
        WHERE ST_DWithin(
            geom::geography, 
            ST_SetSRID(ST_Point($1, $2), 4326)::geography, 
            $3
        )
        """
        records = await connection.fetch(query, lon, lat, radius)
        return [dict(record) for record in records]

# 5. Endpoint POST (Create Data Baru)
@app.post("/api/fasilitas", tags=["Fasilitas"])
async def create_fasilitas(data: FasilitasCreate):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database belum siap")
        
    async with pool.acquire() as connection:
        query = """
        INSERT INTO fasilitas_publik (nama, geom)
        VALUES ($1, ST_SetSRID(ST_Point($2, $3), 4326))
        RETURNING id
        """
        try:
            new_id = await connection.fetchval(query, data.nama, data.longitude, data.latitude)
            return {"status": "success", "id": new_id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
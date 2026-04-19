import docker
import uuid
from fastapi import FastAPI

app = FastAPI()
client = docker.from_env()

DATA_BASE_PATH = "/Users/arpo/minio-data"

@app.post("/instances/create")
async def create_instance():
    instance_id = str(uuid.uuid4())[:8]
    access_key = f"user_{instance_id}"
    secret_key = str(uuid.uuid4())
    
    external_port = 9000 + len(client.containers.list())

    container = client.containers.run(
        "minio/minio",
        command="server /data --console-address :9001",
        name=f"minio-{instance_id}",
        environment={
            "MINIO_ROOT_USER": access_key,
            "MINIO_ROOT_PASSWORD": secret_key
        },
        volumes={f"{DATA_BASE_PATH}/{instance_id}": {'bind': '/data', 'mode': 'rw'}},
        ports={'9000/tcp': external_port, '9001/tcp': external_port + 1000},
        detach=True
    )

    return {
        "instance_id": instance_id,
        "endpoint": f"http://YOUR_IP:{external_port}",
        "access_key": access_key,
        "secret_key": secret_key
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

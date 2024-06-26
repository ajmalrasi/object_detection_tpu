import base64
from fastapi.testclient import TestClient
from PIL import Image
import io
from server import app
client = TestClient(app)

def test_successful_predict():

    image_size = (640, 480)
    color = (255, 0, 0) 
    image = Image.new('RGB', size=image_size, color=color)

    with io.BytesIO() as output:
        image.save(output, format="JPEG")
        image_bytes = output.getvalue()

    image_data = base64.b64encode(image_bytes).decode('utf-8')
    response = client.post("/predict", json={"image": image_data})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "predictions": []}

def test_missing_image():
    response = client.post("/predict", json={}) 
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing 'image' field in request"}

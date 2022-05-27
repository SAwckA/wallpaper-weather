HTTP_PORT = 8000

run: 
	uvicorn backend.main:app --host 0.0.0.0 --port $(HTTP_PORT) --ws-ping-interval 10.0 --ws-ping-timeout 5.0
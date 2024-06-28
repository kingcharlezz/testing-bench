import secrets
import time
import concurrent.futures
from VerifiedModelSession import VerifiedModelSession

MAX_CONCURRENT_REQUESTS = 3

def generate_random_inputs():
    return [secrets.SystemRandom().uniform(-1, 1) for _ in range(5)]

def simulate_proof_request(request_id, model_id):
    public_inputs = generate_random_inputs()
    
    print(f"Request {request_id}: Generated random inputs: {public_inputs}")

    try:
        model_session = VerifiedModelSession(public_inputs=public_inputs, model_id=model_id)
        
        query_output, proof_time = model_session.gen_proof()
        
        print(f"Request {request_id}: Proof generated in {proof_time:.2f} seconds")
        
        proof_string = query_output.get('proof')
        verification_result = model_session.verify_proof_and_inputs(proof_string, public_inputs)
        
        print(f"Request {request_id}: Proof verification result: {'Success' if verification_result else 'Failure'}")

        return verification_result

    except Exception as e:
        print(f"Request {request_id}: Error during proof generation or verification: {e}")
        return False
    
    finally:
        if 'model_session' in locals():
            model_session.end()

def run_continuous_simulation(model_id):
    request_id = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
        while True:
            futures = []
            for _ in range(MAX_CONCURRENT_REQUESTS):
                request_id += 1
                futures.append(executor.submit(simulate_proof_request, request_id, model_id))
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                # You can add additional processing here if needed
            
            print(f"Completed batch of {MAX_CONCURRENT_REQUESTS} requests. Waiting for 10 seconds before next batch...")
            time.sleep(10)  # Wait for 10 seconds before starting the next batch

if __name__ == "__main__":
    test_model_id = [0]  # You can change this to any model ID you want to test
    try:
        run_continuous_simulation(test_model_id)
    except KeyboardInterrupt:
        print("Simulation stopped by user.")

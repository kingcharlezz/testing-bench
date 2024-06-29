import secrets
import json
from VerifiedModelSession import VerifiedModelSession
import time

def generate_random_inputs():
    return [secrets.SystemRandom().uniform(-1, 1) for _ in range(5)]

def simulate_proof_request(model_id):
    # Generate random inputs
    public_inputs = generate_random_inputs()
    
    print(f"Generated random inputs: {public_inputs}")

    try:
        # Create a VerifiedModelSession with random inputs
        with VerifiedModelSession(public_inputs=public_inputs, model_id=model_id) as model_session:
            # Generate the input file
            model_session.gen_input_file()

            # Read and print the input file for debugging
            with open(model_session.input_path, 'r') as f:
                input_data = json.load(f)
                print(f"Input data for witness generation: {input_data}")

            # Generate the proof
            query_output, proof_time = model_session.gen_proof()
            
            # Parse the query output to a dictionary
            query_output = json.loads(query_output)

            print(f"Proof generated successfully:")
            print(f"Query output: {query_output}")
            print(f"Proof time: {proof_time} seconds")
            
            # Extract rescaled outputs from query output
            rescaled_outputs = query_output.get('pretty_public_inputs', {}).get('rescaled_outputs', [])

            # Log results
            log_data = {
                "input_data": [public_inputs],
                "output_data": rescaled_outputs
            }

            with open('proof_log.json', 'a') as log_file:
                json.dump(log_data, log_file)
                log_file.write('\n')

    except Exception as e:
        print(f"Error during proof generation or verification: {e}")

if __name__ == "__main__":
    test_model_id = [0]  # or use PROOF_OF_WEIGHTS_MODEL_ID if you want to test that specifically
    
    while True:
        simulate_proof_request(test_model_id)
        time.sleep(3)  # Adding a delay to avoid overloading the system

from flows.batch_flow import batch_data_flow
from flows.streaming_flow import streaming_data_flow

if __name__ == "__main__":
    batch_data_flow()           # One-time at project start
    streaming_data_flow()       # Can be scheduled repeatedly

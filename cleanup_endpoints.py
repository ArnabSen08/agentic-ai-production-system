import boto3
import sys

def cleanup_all_endpoints():
    print("Starting SageMaker Endpoint Cleanup...")
    sm_client = boto3.client('sagemaker')
    
    # List endpoints
    endpoints = sm_client.list_endpoints(StatusEquals='InService')['Endpoints']
    endpoints += sm_client.list_endpoints(StatusEquals='Creating')['Endpoints']
    endpoints += sm_client.list_endpoints(StatusEquals='Failed')['Endpoints']
    
    if not endpoints:
        print("No endpoints found to delete.")
        return

    print(f"Found {len(endpoints)} endpoints. Deleting...")
    
    for ep in endpoints:
        ep_name = ep['EndpointName']
        print(f"Deleting endpoint: {ep_name}")
        try:
            sm_client.delete_endpoint(EndpointName=ep_name)
            print(f"Deleted {ep_name}")
        except Exception as e:
            print(f"Error deleting {ep_name}: {e}")
            
    print("Cleanup complete. Please wait a few minutes for resources to release.")

if __name__ == "__main__":
    cleanup_all_endpoints()

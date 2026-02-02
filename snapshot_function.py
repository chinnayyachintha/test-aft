import boto3
import os
 
def lambda_handler(event, context):

    region = os.environ["AWS_REGION"]
    ec2 = boto3.client("ec2", region_name=region)
 
    try:
        response = ec2.get_snapshot_block_public_access_state()
        state = response.get("State")
        if state == "unblocked":
            ec2.enable_snapshot_block_public_access(
                State="block-all-sharing"
            )

            return {
                "status": "remediated",
                "region": region,
                "message": "block-all-sharing enabled"
            }
 
        return {
            "status": "compliant",
            "region": region,
            "message": f"Already compliant ({state})"
        }
 
    except Exception as e:
        return {
            "status": "error",
            "region": region,
            "error": str(e)
        }

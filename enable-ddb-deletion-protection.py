import boto3
import logging
import os
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
# Automatically picks the region where Lambda is running
region = os.environ["AWS_REGION"]
dynamodb = boto3.client("dynamodb", region_name=region)
 
 
def lambda_handler(event, context):
    enabled_tables = []
    skipped_tables = []
    failed_tables = []
 
    paginator = dynamodb.get_paginator("list_tables")
 
    for page in paginator.paginate():
        for table_name in page["TableNames"]:
            try:
                response = dynamodb.describe_table(TableName=table_name)
                table = response["Table"]
                was_protected = table.get("DeletionProtectionEnabled", False)
 
                if was_protected:
                    skipped_tables.append(table_name)
                    logger.info(f"[{region}] Skipping {table_name} (already protected)")

                    continue
                dynamodb.update_table(
                    TableName=table_name,
                    DeletionProtectionEnabled=True
                )
 
                enabled_tables.append(table_name)
                logger.info(f"[{region}] Enabled deletion protection for {table_name}")
 
            except Exception as e:
                failed_tables.append({
                    "table": table_name,
                    "error": str(e)
                })

                logger.error(f"[{region}] Failed processing {table_name}: {str(e)}")
 
    return {

        "region": region,
        "summary": {
            "enabled_count": len(enabled_tables),
            "skipped_count": len(skipped_tables),
            "failed_count": len(failed_tables)
        },

        "enabled_tables": enabled_tables,
        "skipped_tables": skipped_tables,
        "failed_tables": failed_tables
    }

 
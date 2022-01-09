#!/usr/bin/env python3
##
#
# The AWS CDK stack APP doest the below function
#   - Create the VPC with two public subnet and two private subnet
#   - Create ECS cluster with auto scaling group and deploy the simple go application.
#   - Create the Application loadbalancer
#   - Grant the permission from s3 to lamda
#

import aws_cdk as cdk
from ecs_elb.elasticcontianerservice_elb_stack import ElasticContainerServiceElbStack

app = cdk.App()
ElasticContainerServiceElbStack(app, "ElasticContainerServiceElbStack",
                env=cdk.Environment(account='235344113908', 
                                    region='us-east-1'),
                )

app.synth()

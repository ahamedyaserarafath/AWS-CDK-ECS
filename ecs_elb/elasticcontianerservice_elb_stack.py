#!/usr/bin/env python3
##
# The AWS CDK stack APP doest the below function
#   - Create the VPC with two public subnet and two private subnet
#   - Create ECS cluster with auto scaling group and deploy the simple go application.
#   - Create the Application loadbalancer with target groups
#

from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    Duration, CfnOutput, Stack
)

import json
from constructs import Construct


class ElasticContainerServiceElbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str , **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a cluster
        vpc = ec2.Vpc(
            self, "MyVpc",
            max_azs=2,
        )

        # Create a ECS cluster
        cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

        # Create Auto scalling group with t2.micro
        asg = autoscaling.AutoScalingGroup(
            self, "DefaultAutoScalingGroup",
            instance_type=ec2.InstanceType.of(
                                ec2.InstanceClass.BURSTABLE2,
                                ec2.InstanceSize.MICRO,),
            
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )

        capacity_provider = ecs.AsgCapacityProvider(self, "AsgCapacityProvider",
            auto_scaling_group=asg
        )
        cluster.add_asg_capacity_provider(capacity_provider)

        # Create Task Definition with simple factorial app from DockerHub
        task_definition = ecs.Ec2TaskDefinition(
            self, "TaskDef")
        container = task_definition.add_container(
            "web",
            image=ecs.ContainerImage.from_registry("ahamedyaserarafath/simple-factorial-goapp"),
            memory_limit_mib=256
        )
        # Map the port to 80
        port_mapping = ecs.PortMapping(
            container_port=80,
            host_port=80,
            protocol=ecs.Protocol.TCP
        )
        container.add_port_mappings(port_mapping)

        # Create ECS Service
        service = ecs.Ec2Service(
            self, "Service",
            cluster=cluster,
            task_definition=task_definition
        )

        # Create Application loadbalancer for ECS
        lb = elbv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True
        )
        # Add the public listerner port
        listener = lb.add_listener(
            "PublicListener",
            port=80,
            open=True
        )
        # Add the health check to make sure target group are up and running 
        health_check = elbv2.HealthCheck(
            interval=Duration.seconds(60),
            path="/health",
            timeout=Duration.seconds(5)
        )

        # Attach ALB to ECS Service
        listener.add_targets(
            "ECS",
            port=80,
            targets=[service],
            health_check=health_check,
        )

        CfnOutput(
            self, "LoadBalancerDNS",
            value=lb.load_balancer_dns_name
        )
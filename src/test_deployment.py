from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import Ec2Client


def main():
    # create a vpc
    ec2_client = Ec2Client().get_client()
    vpc = VPC(ec2_client)
    vpc_response = vpc.create_vpc()
    print('VPC created :' + str(vpc_response))

    # Add name tag to VPC
    vpc_name = 'Boto3-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)
    print('Added' + vpc_name+ 'to' + vpc_id)

    # Create IGW
    igw_responce = vpc.create_internet_gateway()
    igw_id = igw_responce['InternetGateway']['InternetGatewayId']
    vpc.attach_igw_to_vpc(vpc_id,igw_id)
    print('Added' + vpc_id + 'to' + igw_id)

    # Create a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/16')
    public_subnet_id = public_subnet_response['Subnet']['SubnetID']

    print('subnet created for VPC '+ vpc_id+ ' : ' + str(public_subnet_response))

    # Add name tag to public subnet
    vpc.add_name_tag(public_subnet_id, 'Boto3-Public-Subnet')

    # create public route table
    public_route_table_response = vpc.create_public_route_table(vpc_id)
    rtb_id = public_route_table_response['RouteTable']['RouteTableId']
    # adding the IGW to public route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)
    # Associate public subnet with route table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

    # allow auto assign public ip address for subnet
    vpc.allow_auto_assign_ip_address_for_subnet(public_subnet_id)

    # Create a private subnet
    private_subnet_response =  vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']
    print('created private for VPC ' + private_subnet_id + ' : ' + vpc_id)

    # Add name tag to private subnet
    vpc.add_name_tag(private_subnet_id, 'Boto3-Private-Subnet')


    # Create EC2
    ec2 = EC2(ec2_client)
    # Create a KEY-PAIR
    key_pair_name = 'Boto3-Keypair'
    key_pair_response = ec2.create_key_pair(key_pair_name)
    print('created Key pair with name ' + str(key_pair_response))



if __name__ == "__main__":
    main()

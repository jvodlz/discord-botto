import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda"
import * as ssm from "aws-cdk-lib/aws-ssm"

export class DiscordBottoStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const discordPublicKey = ssm.StringParameter.fromStringParameterAttributes(this, 
      "PublicKey", {
        parameterName: "/discord/botto/public/key",
      }
    );

    const dockerFunction = new lambda.DockerImageFunction(
      this, "DockerFunction", {
        code: lambda.DockerImageCode.fromImageAsset("./src"),
        memorySize: 1024,
        timeout: cdk.Duration.seconds(10),
        environment: {
          PUBLIC_KEY: discordPublicKey.stringValue
        },
    });

    const functionUrl = dockerFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedOrigins: ["*"],
        allowedMethods: [
          lambda.HttpMethod.GET,
          lambda.HttpMethod.POST,
          lambda.HttpMethod.PATCH
        ],
        allowedHeaders: ["*"]
      }
    });

    new cdk.CfnOutput(this, "FunctionUrl", {
      value: functionUrl.url
    });

  }
}

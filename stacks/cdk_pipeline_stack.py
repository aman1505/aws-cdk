from aws_cdk import( 
    aws_s3 as s3,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipelineactions,
    aws_codebuild as codebuild,
    core as cdk
    )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Creating an empty pipeline 
        pipeline = codepipeline.Pipeline(self, "MyCDKPipeline",
            pipeline_name="MyCDKPipeline"
        )

        #Creating a source stage with GitHub as source 
        source_output = codepipeline.Artifact()
        source_action = codepipelineactions.GitHubSourceAction(
            action_name="GitHub_Source",
            owner="aman1505",
            repo="cdk-practice",
            oauth_token=cdk.SecretValue.secrets_manager("my-github-token",json_field='my-github-token'),
            output=source_output,
            branch="main"
        )

        #Adding Source stage created in previous 
        pipeline.add_stage(
            stage_name="Source",
            actions=[source_action]
        )

        # Creating BuildSpec file for Stage Build and action CodeBuildS3 calling it as project for CdkPracticeStack
        stack_name = "CdkS3Stack"
        project_s3Stack = codebuild.PipelineProject(self, "MyProjectS3",
                build_spec=codebuild.BuildSpec.from_object({
                    "version":"0.2",
                    "phases":{
                        "install": {
                            "commands": [
                                "echo 'starting installation'"
                                "npm install aws-cdk",
                                "npm update",
                                "pip install -r requirements.txt"
                            ]
                        },
                        "build":{
                            "commands": [
                                "echo 'starting build stage'"
                                f"npx cdk deploy {stack_name}"
                            ]
                        }
                    }
                }
                ),
                environment={
                    "build_image": codebuild.LinuxBuildImage.STANDARD_2_0
                }
            )

        # Creating BuildSpec file for Stage Build and action CodeBuildLambda calling it as project for CdkPracticeStack
        stack_name = "CdkLambdaStack"
        project_lambdaStack = codebuild.PipelineProject(self, "MyProjectLambda",
                build_spec=codebuild.BuildSpec.from_object({
                    "version":"0.2",
                    "phases":{
                        "install": {
                            "commands": [
                                "echo 'starting installation'"
                                "npm install aws-cdk",
                                "npm update",
                                "pip install -r requirements.txt"
                            ]
                        },
                        "build":{
                            "commands": [
                                "echo 'starting build stage'"
                                f"npx cdk deploy {stack_name}"
                            ]
                        }
                    }
                }
                ),
                environment={
                    "build_image": codebuild.LinuxBuildImage.STANDARD_2_0
                }
            )

        #Creating action codeBuildS3 for stage Build 
        build_action_s3 = codepipelineactions.CodeBuildAction(
            action_name="CodeBuildS3",
            project=project_s3Stack,
            input=source_output, # The build action must use the CodeCommitSourceAction output as input.
            outputs=[codepipeline.Artifact()]
        )    

        #Creation action codeBuildLambda for stage Build
        build_action_lambda = codepipelineactions.CodeBuildAction(
            action_name="CodeBuildLambda",
            project=project_lambdaStack,
            input=source_output, # The build action must use the CodeCommitSourceAction output as input.
            outputs=[codepipeline.Artifact()]
        )

        #Creating Build stage and adding build_action_s3 in it 
        pipeline.add_stage(
            stage_name="Build",
            actions=[build_action_s3, build_action_lambda]
        )


    

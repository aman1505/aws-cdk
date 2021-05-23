from aws_cdk import( 
    aws_s3 as s3,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipelineactions,
    aws_codebuild as codebuild,
    aws_iam as iam,
    core as cdk
    )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class BuildProjects(cdk.Stack):

    @staticmethod
    def getProjectDefination(self, stack_name, environemt, project_name ):
        project = codebuild.PipelineProject(self, project_name,
            project_name=project_name,
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version":"0.2",
                    "phases":{
                        "install": {
                            "commands": [
                                "echo 'starting installation'",
                                "npm install aws-cdk",
                                "npm update",
                                "pip install -r requirements.txt"
                            ]
                        },
                        "build":{
                            "commands": [
                                "echo 'starting build stage'",
                                f"npx cdk deploy {stack_name}"
                            ]
                        }
                    }
                }
            )
        )
        return project
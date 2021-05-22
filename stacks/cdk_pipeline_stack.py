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
from utils.buildProjects import BuildProjects 

class CdkPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Creating an empty pipeline 
        # pipeline = codepipeline.Pipeline(self, "MyCDKPipeline",
        #     pipeline_name="MyCDKPipeline"
        # )
        
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
        # pipeline.add_stage(
        #     stage_name="Source",
        #     actions=[source_action]
        # )

        module_list = ["CdkPipelineStack", "CdkS3Stack"]
        environemt = "dev"
        action_list=[]

        # Iterating over the module list and creating code build project 
        for module in module_list: 
            project_name = module+"-"+environemt
            project = BuildProjects.getProjectDefination(self, module, environemt, project_name)
            project.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AdministratorAccess'))
            action = codepipelineactions.CodeBuildAction(
            action_name="CodeBuild"+module,
            project=project,
            input=source_output, # The build action must use the CodeCommitSourceAction output as input.
            outputs=[codepipeline.Artifact()]
            )
            action_list.append(action)

        #Creating Build stage and adding build_action_s3 in it 
        # pipeline.add_stage(
        #     stage_name="Build",
        #     actions=action_list
        # )
        # codepipeline.Pipeline(self, "MyCDKPipeline",
        #     pipeline_name="MyCDKPipeline",
        #     stages=[{
        #     "stage_name": "Source",
        #     "actions": [source_action]
        #     },
        #     {
        #     "stage_name": "Build",
        #     "actions": action_list
        #     }   
        #    ]
        # )

        codepipeline.Pipeline(self, "Pipeline",
            stages=[
                codepipeline.StageProps(stage_name="Source",
                    actions=[source_action]),
                codepipeline.StageProps(stage_name="Build",
                    actions=action_list
                )
            ], pipeline_name= "MyCDKPipeline"
        )
        
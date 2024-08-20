## Important steps

How to create a new branch, standard conversion is feature/name of the feature: <br>
$ git branch 'feature/name of the branch' 

How to go inside of that branch: <br>
$ git checkout 'name of the branch'

- If branch exist, it enters that branch, if not it creates the branch first and goes inside of that branch: <br>
$ git checkout -b 'name of the branch'

### FLASK
Model- define the tables(models and schemas) and relationship between tables. <br>
Controller - Perform operations on DB/ input e.g functions/ routes


* Password should be excluded from the schema objects, eg: exclude=["Password"]

## Pull request GIT

    1 - In main branch, click on compare and pull request. In case of conflicts you need to resolve them first.
    2 - Click on 'Create pull request' and confirm it.
    3 - Change branch back to main and perform git pull.
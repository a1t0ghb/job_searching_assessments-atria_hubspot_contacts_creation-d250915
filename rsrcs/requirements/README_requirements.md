# 🚧 TODO 🚧

- Rebuild WHOLE document; i.e. review process, rewrite commands, review files structure, etc.
- Updated commands, run from **root folder**; e.g. '/workspaces/job_searching_assessments-atria_hubspot_contacts_creation-d250915'.

```bash
# [root folder]

pipreqs --savepath='rsrcs/requirements/_support_files/requirements_production-pipreqs.in' '.'  # scans 'py3-atria_hubspot_contacts_creation.py', since it runs on root folder.
pip-compile -o 'rsrcs/requirements/requirements_production-pipreqs.txt' 'rsrcs/requirements/_support_files/requirements_production-pipreqs.in' --strip-extras
pip-compile -o 'rsrcs/requirements/requirements_production.txt' 'rsrcs/requirements/_support_files/requirements_production.in' --strip-extras
pip-compile -o 'rsrcs/requirements/requirements_development.txt' 'rsrcs/requirements/_support_files/requirements_development.in' --strip-extras
pip freeze > './rsrcs/requirements/requirements_development-pip_freeze.txt'
```

# MANAGING DEPENDENCIES AND CREATING **'requirements.txt'** FILES.

- The **'requirements.txt'** file is the regular convention for setting up dependencies with **'pip'**, but in this case, we'll split it into 2 files for appropiate management:
  - **'requirements_prod.in'**: for production stage (which will create a **'requirements_prod.txt'** file).
  - **'requirements_dev.in'**: for development stage (which will create a **'requirements_dev.txt'** file).
  - Ref.: '<https://andypickup.com/developing-in-python-with-dev-containers-part-1-setup-f1aeb89cbfed>'.
  - Ref.: '<https://github.com/jazzband/pip-tools?tab=readme-ov-file#workflow-for-layered-requirements>'.
- **NOTES:**
  - To create both 'requirements' files, we'll be using the dependency **'pip-tools'**.
    - Ref.: '<https://dev.to/sajidurshajib/do-not-use-pip-freeze-1ikc>'.
    - Ref.: '<https://github.com/jazzband/pip-tools?tab=readme-ov-file#requirements-from-requirementsin>'.
  - The file for production stage will function as an *'anchor' / 'constraint'* for setting up the dependencies of the development stage.
    - Ref.: '<https://github.com/jazzband/pip-tools?tab=readme-ov-file#workflow-for-layered-requirements>'.
    - Ref.: '<https://luminousmen.com/post/pip-constraints-files>'.

# FILE STRUCTURE.

- **[working_dir]**                                   : e.g.: **'/workspaces/VSCode-DevContainers-Python_MediumFastAPI_d250108'**.
  - **'_README.md'**                                  : **'.md'** file with notes, SPECIFIC to project.
  - **'imgs'**                                        : directory for storing images of **'.md'** files.
    - **[img01]**                                     : e.g. **'img_README_APIItemID.png'**
    - **[img02]**
    - **[other images]**
  - **'.devcontainer'**                               : directory specific for vs code - dev. containers.
    - **'devcontainer.json'**
    - **'postCreateCommand.sh'**                      : bash file to execute additional commands, not considered in the Dockerfile of the dev. container. In this case, installing dependencies from **'requirements_prod.txt'** *and / or* **'requirements_dev.txt'**. <u>[Requires manual adjustment by user](/requirements/_requirements.md#41-define-if-its-required-to-move-to-prod-stage-or-keep-developing-and-adjust-code-accordingly-in-postcreatecommandsh-file)</u>.
  - **'requirements'**
    - **'_requirements.md'**                          : *this file*.
    - **'_requirements_prod-template_v250118.in'**    : e.g. file version of 2025.01.18.
    - **'_requirements_dev-template_v250118.in'**
    - **'requirements_prod.in'**                      : source file to [create **'requirements_prod.txt'**, using dependency **'pip-tools'**](/requirements/_requirements.md#2-update-requirements_prodin-file).
    - **'requirements_dev.in'**                       : source file to [create **'requirements_dev.txt'**, using dependency **'pip-tools'**](/requirements/_requirements.md#3-update-requirements_devin-file).
    - **'requirements_prod-pipreqs.in'**              : 'requirements' file generated using [**'pipreqs'** approach](/requirements/_requirements.md#12-if-not-manually-keeping-track-of-dependencies-but-instead-relying-only-on-main-files-eg-mainpy-jupyter-notebooks-etc-and-their-import-statements).
    - **'requirements_freeze.txt'**                   : 'requirements' file generated using [**'pip freeze'**](/requirements/_requirements.md#5-optional-freeze-your-environment-with-pip), to store it as REFERENCE ONLY.
  - **'requirements_dev.txt'**                        : 'requirements' file used by **'postCreateCommand.sh'**
  - **'requirements_prod.txt'**                       : 'requirements' file used by **'postCreateCommand.sh'**
  - **[other files]**                                 : other files, such as **'main.py'**, jupyter notebooks, etc.

# STEPS.

> **IMPORTANT:** all commands are assumed to be executed in the root folder (e.g. **'/workspaces/VSCode-DevContainers-Python_MediumFastAPI_d250108'**), as the CURRENT WORKING DIRECTORY.

## 1. First boot / starting development.

- Install **'pip-tools'**, via Terminal > `$ pip install pip-tools`.

### 1.2. If not manually keeping track of dependencies, but instead relying ONLY on main files (e.g. **'main.py'**, jupyter notebooks, etc.) and their 'import' statements.

- <u>This approach is valid for getting ONLY PRODUCTION dependencies, based on 'import' statements.</u>
- Install **'pipreqs'**, if not already installed, via Terminal > `$ pip install pipreqs`.
- Create **'requirements_prod-pipreqs.in'** file by running via Terminal > `$ pipreqs --savepath='requirements/requirements_prod-pipreqs.in' '.'`.
- (OPTIONAL) Adjust **'requirements_prod.in'** file with data from previously created file **'requirements_prod-pipreqs.in'**.

## 2. Update **'requirements_prod.in'** file.

- Start with template **'_requirements_prod-template_v250118.in'**, by duplicating it, and changing it's name to **'requirements_prod.in'**.
- Adjust file: include dependencies that will be part of the version for production.
  - **NOTE:** dependencies list can be obtained either via a) keeping track of them manually, or b) using [**'pipreqs'** approach](/requirements/_requirements.md#12-if-not-manually-keeping-track-of-dependencies-but-instead-relying-only-on-main-files-eg-mainpy-jupyter-notebooks-etc-and-their-import-statements).
- Create **'requirements_prod.txt'** file by running via Terminal > either:
  - `$ pip-compile -o 'requirements_prod.txt' 'requirements/requirements_prod-pipreqs.in'`, if using [**'pipreqs'** approach](/requirements/_requirements.md#12-if-not-manually-keeping-track-of-dependencies-but-instead-relying-only-on-main-files-eg-mainpy-jupyter-notebooks-etc-and-their-import-statements).
  - `$ pip-compile -o 'requirements_prod.txt' 'requirements/requirements_prod.in'`, otherwise.
- Run following code to add comment (*at the beginning of the file*) of **'requirements_prod.txt'**, regarding direct vs. indirect dependencies:

``` bash
# sed: add tex in 1st line, at the beginning of a file.
# - Ref.: 'https://superuser.com/questions/246837/how-do-i-add-text-to-the-beginning-of-a-file-in-bash'.
# Escape characters in sed.
# - Ref.: 'https://unix.stackexchange.com/questions/32907/what-characters-do-i-need-to-escape-when-using-sed-in-a-sh-script'
sed -i "1s/^/\
#\n\
# Direct \/ main dependencies, with comment: 'via -r requirements\/requirements_prod.in'.\n\
# Otherwise, it's an indirect \/ transitive dependency, to use as 'constraint'.\n\
#\n\
# ---\n\
/" requirements_prod.txt

# COMMENT FOR REFERENCE:
#
# Direct / main dependencies, with comment: 'via -r requirements/requirements_prod.in'
# Otherwise, it's an indirect / transitive dependency, to use as 'constraint'.
#
# ---
```

## 3. Update **'requirements_dev.in'** file.

- Start with template **'_requirements_dev-template_v250118.in'**, by duplicating it, and changing it's name to **'requirements_dev.in'**.
- Adjust file: include dependencies that will be used ONLY when developing, such as helpers, wrappers, etc.; e.g. **'pipreqs'**, **'pip-tools'**, etc.
  - **NOTE:** remember [**'pipreqs'** approach](/requirements/_requirements.md#12-if-not-manually-keeping-track-of-dependencies-but-instead-relying-only-on-main-files-eg-mainpy-jupyter-notebooks-etc-and-their-import-statements) WON'T provide any helper dependency that is not declared in any of the 'import' statements.
- Create **'requirements_dev.txt'** file by running via Terminal > `$ pip-compile -o 'requirements_dev.txt' 'requirements/requirements_dev.in'`.

> **IMPORTANT:** remember to make sure this dev. file has the constraint of the [prod. file](/requirements/_requirements.md#1-first-boot--starting-development); i.e. has the code line `--constraint '../requirements_prod.txt'`.

- Run following code to add comment (*at the beginning of the file*) of **'requirements_dev.txt'**, regarding direct vs. indirect dependencies:

``` bash
# sed: add tex in 1st line, at the beginning of a file.
# - Ref.: 'https://superuser.com/questions/246837/how-do-i-add-text-to-the-beginning-of-a-file-in-bash'.
# Escape characters in sed.
# - Ref.: 'https://unix.stackexchange.com/questions/32907/what-characters-do-i-need-to-escape-when-using-sed-in-a-sh-script'
sed -i "1s/^/\
#\n\
# Direct \/ main dependencies, with comment: 'via -r requirements\/requirements_dev.in'.\n\
# Otherwise, it's an indirect \/ transitive dependency, to use as 'constraint'.\n\
#\n\
# ---\n\
/" requirements_dev.txt

# COMMENT FOR REFERENCE:
#
# Direct / main dependencies, with comment: 'via -r requirements/requirements_dev.in'
# Otherwise, it's an indirect / transitive dependency, to use as 'constraint'.
#
# ---
```

**FOOTNOTE on appending text to files in Linux**
- You can append text to the END of a file (not to the beggining, as previously), using **'cat'** command; e.g. if wanted to append previous reference comment at the end.
- Ref.: '<https://www.tutorialspoint.com/writing-text-to-file-using-linux-cat-command>'.

``` bash
cat >> 'requirements.txt' << EOF
#
# Direct / main dependencies, with comment: 'via -r requirements/requirements_dev.in'
# Otherwise, it's an indirect / transitive dependency, to use as 'constraint'.
#
# ---
EOF
```

## 4. (OPTIONAL) Rebuild dev. container.

- Rebuilding the container is a good practice, to get used to fill 'requirements' files and compile them, instead of only using `$ pip install <package>`.

> **NOTE:** remember dependencies installed ONLY via `$ pip install <package>`, without adding to the 'requirements' files, will be lost if the container stops, is deleted, or rebuilt.

### 4.1. Define if it's required to move to prod. stage or keep developing, and adjust code accordingly in **'postCreateCommand.sh'** file.

``` bash
# Choose one line, either this one for development:
pip install --requirement 'requirements_prod.txt' --requirement 'requirements_dev.txt' # To install requirements in dev. stage (DEFAULT).

# Or this one, for production:
pip install --requirement 'requirements_prod.txt' # To install requirements in prod. stage.
```

### 4.2. Rebuild dev. container: open command palette (`<F1>`, or `<Ctrl>` + `<Shift>` + `<P>`) > "Rebuild Container".

## 5. (OPTIONAL) Freeze your environment with **'pip'**.

- Run `$ pip freeze > 'requirements/requirements_freeze.txt'` to use it as REFERENCE / COMPLEMENT ONLY, if there are any issues with **'requirements_prod.txt'** or **'requirements_dev.txt'**.

> **NOTE:** remember **'pip freeze'** has several 'disadvantages' such as a) it only saves packages that are installed with **'pip install'**, and b) it saves ALL packages that are currently installed in the environment, even if they are not imported / used in your current project. Ref.: '<https://github.com/bndr/pipreqs?tab=readme-ov-file#why-not-pip-freeze>'.

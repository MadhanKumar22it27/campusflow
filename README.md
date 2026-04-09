### Campusflow

Campus Management System

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app campusflow
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/campusflow
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

### Understanding

1) Workflows

    - A workflow is a controlled approval system that tells how the work should be proceed and   what are the steps will be followed

2) Role-based Permissions + has_permission hooks

    - It is used to give the access to particular documents for particular users such as admin, staffs, customers and etc

    ```code

    def student_query(user):
    roles = frappe.get_roles(user)

    if "Campus Admin" in roles:
        return ""

    if "Teacher" in roles:
        return ""

    if "Parent" in roles:
        return f"`tabStudent`.parent_name = {frappe.db.escape(user)}"

    return ""

    ```
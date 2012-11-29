from django_rules import utils

rules_list = [
              {'codename': 'can_read_job', 'model': 'Job'},
              ]

for rule in rules_list:
    utils.register(app_name='tao', **rule)

# After each rule addition/edit
# remove all rules ( [rule.delete() for rule in django_rules.models.RulePermission.objects.all()] )
# bin/django sync_rules  # creates new rules
# bin/django dumpdata django_rules.rulepermission --natural > tao/fixtures/rules.json  # creates rule fixture for test cases
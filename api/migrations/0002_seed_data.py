from django.db import migrations


def seed_data(apps, schema_editor):
    CustomUser = apps.get_model('api', 'CustomUser')
    TimeRecord = apps.get_model('api', 'TimeRecord')
    from django.utils import timezone
    from django.contrib.auth.hashers import make_password

    users_data = [
        {
            'employee_id': 'ADM001',
            'first_name': 'Admin',
            'last_name': 'Sistema',
            'email': 'admin@timetracker.com',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'password': make_password('Pbkdf2@1234'),
        },
        {
            'employee_id': 'EMP001',
            'first_name': 'Ana',
            'last_name': 'Silva',
            'email': 'ana.silva@timetracker.com',
            'role': 'employee',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
            'password': make_password('Pbkdf2@1234'),
        },
        {
            'employee_id': 'EMP002',
            'first_name': 'Bruno',
            'last_name': 'Oliveira',
            'email': 'bruno.oliveira@timetracker.com',
            'role': 'employee',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
            'password': make_password('Pbkdf2@1234'),
        },
        {
            'employee_id': 'EMP003',
            'first_name': 'Carla',
            'last_name': 'Souza',
            'email': 'carla.souza@timetracker.com',
            'role': 'employee',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
            'password': make_password('Pbkdf2@1234'),
        },
        {
            'employee_id': 'EMP004',
            'first_name': 'Diego',
            'last_name': 'Ferreira',
            'email': 'diego.ferreira@timetracker.com',
            'role': 'employee',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
            'password': make_password('Pbkdf2@1234'),
        },
    ]

    created_users = {}
    now = timezone.now()
    for udata in users_data:
        udata['date_joined'] = now
        user, created = CustomUser.objects.get_or_create(employee_id=udata['employee_id'], defaults=udata)
        if not created:
            # Update existing
            for k, v in udata.items():
                setattr(user, k, v)
            user.save()
        created_users[user.employee_id] = user

    emp = created_users.get('EMP001')
    if emp:
        today = timezone.localdate()
        sleep = timezone.timedelta
        records = [
            (today - sleep(days=1), '08:00', '17:00'),
            (today - sleep(days=2), '08:30', '17:30'),
            (today - sleep(days=3), '09:00', '18:00'),
        ]
        for date_val, in_h, out_h in records:
            clock_in = timezone.make_aware(timezone.datetime.combine(date_val, timezone.datetime.strptime(in_h, '%H:%M').time()))
            clock_out = timezone.make_aware(timezone.datetime.combine(date_val, timezone.datetime.strptime(out_h, '%H:%M').time()))
            TimeRecord.objects.update_or_create(
                user=emp,
                date=date_val,
                defaults={
                    'clock_in': clock_in,
                    'clock_out': clock_out,
                    'observation': 'Registro inicial via migration',
                },
            )


def unseed_data(apps, schema_editor):
    CustomUser = apps.get_model('api', 'CustomUser')
    TimeRecord = apps.get_model('api', 'TimeRecord')

    TimeRecord.objects.filter(user__employee_id='EMP001').delete()
    CustomUser.objects.filter(employee_id__in=['ADM001','EMP001','EMP002','EMP003','EMP004']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]

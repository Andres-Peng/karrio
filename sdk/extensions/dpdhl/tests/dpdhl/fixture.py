import karrio

gateway = karrio.gateway["dpdhl"].create(
    dict(
        username="username",
        password="password",
        signature="pass",
        app_id="app_01",
        account_number="2222222222",
    )
)

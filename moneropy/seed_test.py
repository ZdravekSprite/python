from monero.seed import Seed

s = Seed("fewest lipstick auburn cocoa macro circle hurried impel macro hatchet jeopardy swung aloof spiders gags jaws abducts buying alpine athlete junk patio academy loudly academy")

print(s.secret_spend_key())
# '0b7a7bac8a5b6de2f483d703ef82b1bb3e37dd834006d02140a6a762b9142d00'

print(s.secret_view_key())
# '75ec665f4912cec813ff7f20bc75b1f375ee2f8d4bb7631ae8d1af302732a609'

print(s.public_spend_key())
# 'd5db200426637399f0076090dea01394afc2b157f94d287516911dbbcf8b2275'

print(s.public_view_key())
# 'cd235f236224b8a5f1e12568927e01a2879bfd49cec2517b0717adb97fe8ae39'

print(s.public_address())
# '49j9ikUyGfkSkPV8TY66p2RsSs6xL7NR5LauJTt7y6LZLhpakUnjcddUksdDgccVPEUBk2obnM1YUMaXKsGsCnow7WYjktm'
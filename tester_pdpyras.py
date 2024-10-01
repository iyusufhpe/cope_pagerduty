from pdpyras import APISession
from token_getter import api_token


# Create the APISession
session = APISession(api_token)

# Disable SSL verification for the session
session.verify = False


print(session.api_key)


# for x in session.iter_all('users'):
#     print(x)
#     break

# print(f"session.api_call_counts: {session.api_call_counts}")

print("\n\n\n")
print("Incident detail: \n")
res = session.rget('/incidents/Q23RA58KK63575/alerts')
print(res)
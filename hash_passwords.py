import streamlit_authenticator as stauth

# Hashage d’une liste de mots de passe
hashed_passwords = stauth.Hasher.hash_list(['motdepasse1', 'motdepasse2', 'motdepasse3'])
print(hashed_passwords)





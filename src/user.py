class User:
    """Luokka, joka kuvastaa tietokannassa olevaa käyttäjää.

    Attributes:
        username: Käyttäjänimi
        passwd: Käyttäjän salasana
        user_id: Käyttäjän id
    """

    def __init__(self, username, passwd, user_id):
        """Konstruktori, joka luo uuden käyttäjäobjektin argumenttien perusteella.

        Args:
            username: Käyttäjänimi
            passwd: Käyttäjän salasana
            user_id: Käyttäjän id
        """
        self.username = username
        self.passwd = passwd
        self.user_id = user_id

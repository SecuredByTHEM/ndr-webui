'''Users who access the WebUI component of NDR'''

from enum import Enum

import bcrypt
import ndr_webui
import ndr_server


class User(object):
    '''Represents a user who can log into the system and (possibly) manage recorders'''

    def __init__(self, nsc):
        self.nsc = nsc
        self.username = None
        self.email = None
        self.real_name = None
        self.password_hash = None
        self.pg_id = None
        self.org_id = None
        self.active = False
        self.superadmin = False

    @classmethod
    def from_dict(cls, nsc, user_dict):
        '''Creates a user object from a dictionary'''
        user_obj = User(nsc)

        user_obj.username = user_dict['username']
        user_obj.email = user_dict['email']
        user_obj.real_name = user_dict['real_name']
        user_obj.password_hash = user_dict['password_hash']
        user_obj.pg_id = user_dict['id']
        user_obj.active = user_dict['active']
        user_obj.superadmin = user_dict['superadmin']

        return user_obj

    @classmethod
    def read_by_username(cls, nsc, username, db_conn):
        '''Gets a user account by email address'''

        return cls.from_dict(nsc,
                             nsc.database.run_procedure_fetchone(
                                 "webui.select_user_by_username",
                                 [username],
                                 existing_db_conn=db_conn))

    @classmethod
    def read_by_email(cls, nsc, email, db_conn):
        '''Gets a user account by email address'''

        return cls.from_dict(nsc,
                             nsc.database.run_procedure_fetchone(
                                 "webui.select_user_by_email",
                                 [email],
                                 existing_db_conn=db_conn))

    @classmethod
    def read_by_id(cls, nsc, user_id, db_conn):
        '''Gets a user by ID number'''

        return cls.from_dict(nsc,
                             nsc.database.run_procedure_fetchone(
                                 "webui.select_user_by_id",
                                 [user_id],
                                 existing_db_conn=db_conn))

    @classmethod
    def create(cls, nsc, creating_user, username, email, password, real_name, db_conn):
        '''Creates a new user. This action must be authorized by an admin user or
           similar'''

        # Check that our creating user can actually do this
        User.check_user_permissions_for_action(
            nsc, creating_user, UserAdminActions.CREATE_USER, db_conn
        )

        # We're good, crypt the password and create the user object
        crypted_pw = str(bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt()), 'utf-8')

        pg_id = nsc.database.run_procedure_fetchone(
            "admin.create_user",
            [username, email, crypted_pw, real_name],
            existing_db_conn=db_conn
        )[0]

        return cls.read_by_id(nsc, pg_id, db_conn)

    @property
    def is_active(self):
        '''Is the user account active and validated?'''
        return self.active

    @property
    def is_anonymous(self):
        '''Is user anonymous (never used)'''
        return False

    @property
    def is_authenticated(self):
        '''Is this user authenticated to login'''
        return True

    def get_id(self):
        '''Return a unique identifer for this user'''
        return self.pg_id

    def check_password(self, password):
        '''Checks that the password is valid for a given user'''

        # I'd technically prefer to do this in the database as I feel like the PW hash
        # algo and such is an implementation detail, but it's always best practice to hash
        # the PW at the first possible point so here it is.

        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password_hash, 'utf-8')):
            return True

        return False

    @staticmethod
    def check_user_permissions_for_action(nsc, user, action, db_conn):
        '''Checks that a user can perform an administrative action'''

        # Checks if we can perform an action, raises exception if we can't
        nsc.database.run_procedure("webui.check_user_permissions_for_action",
                                   [user.pg_id, action.value],
                                   existing_db_conn=db_conn)
        return True

    def get_organizations_for_user(self, db_conn=None):
        '''Retrieves all organizations this user can access and returns a list of them'''

        cursor = self.nsc.database.run_procedure("webui.get_organizations_for_user",
                                                 [self.pg_id],
                                                 existing_db_conn=db_conn)
        organizations = []
        for record in cursor.fetchall():
            organizations.append(
                ndr_webui.OrganizationACL.from_dict(self.nsc, record)
            )

        return organizations


    def get_sites_in_organization_for_user(self, org, db_conn=None):
        '''Retrieves all sites in an organization this user can access and returns a list of them'''

        cursor = self.nsc.database.run_procedure("webui.get_sites_in_organization_for_user",
                                                 [self.pg_id, org.pg_id],
                                                 db_conn)
        sites = []
        for record in cursor.fetchall():
            sites.append(
                ndr_server.Site.from_dict(self.nsc, record)
            )

        return sites

class UserAdminActions(Enum):
    '''Admin actions a user can take'''
    CREATE_USER = 'create_user'

#!/usr/bin/perl
use WebminCore;
init_config();

sub print_error {
    my ( $msg, $submsg ) = @_;

    print ui_print_header(undef, 'Error', '', undef, 0, 1);

    print ui_form_start('../index.cgi', 'get');
    print ui_subheading($msg);
    print ui_subheading($submsg);
    print ui_hr;
    print ui_submit("Return");
    print ui_form_end();

    print ui_print_footer();
    return;
}

sub print_redirect {
    my ( $msg, $submsg ) = @_;
    print ui_print_header(undef, $msg, '', undef, 1, 1);
    print ui_form_start('../index.cgi', 'get');
    print ui_subheading($submsg);
    print ui_submit("Return");
    print ui_form_end();

    print ui_print_footer();
    return;
}

foreign_require("acl");

my ($name, $passwd, $uid, $gid, $quota, $comment, $gcos, $dir, $shell) = getpwnam($remote_user);
if ($uid == 1000) {
    # For form-data
    ReadParseMime();
    if ($in{'action'} eq 'Create User') {
        my $username = $in{'username'};
        my $password = $in{'password'};

        # Check if user already exists
        my @users = acl::list_users();
        my ($user) = grep { $_->{'name'} eq $username } @users;
        if ($user) {
            print_error("Create Linux User", "User '$username' already exists.");
        } else {
            my $newuser = {
                'name' => $username,
                'pass' => acl::encrypt_password($password),
                'modules' => [ 'docker-bedrock' ],
                'rbacdeny' => 0,
                'readonly' => 1};
            if (acl::create_user($newuser)) {
                print_error("Create Linux User", "Failed to create user '$username'.");
            } else {
                print_redirect('Success');
            }
        }
    } elsif ($in{'action'} eq 'Create Group') {
        my $groupname = $in{'groupname'};

        # Check if group already exists
        my ($existing_group) = grep { $_->{'name'} eq $groupname } acl::list_groups();
        if ($existing_group) {
            print_error("Create Webmin Group", "Webmin group '$groupname' already exists.");
        } else {
            # Create the group with access to your module
            my $group = {
                'name' => $groupname,
                'modules' => [ 'docker-bedrock' ] };
            if (acl::create_group($group)) {
                print_error("Create Webmin Group", "Error creating Webmin group: $group_err");
            } else {
                print_redirect('Success');
            }
        }
    } elsif ($in{'action'} eq 'Create Group & Add User') {
        my $username = $in{'username'};
        my $groupname = $in{'groupname'};

        # Check if group already exists
        my ($existing_group) = grep { $_->{'name'} eq $groupname } acl::list_groups();
        if ($existing_group) {
            print_error("Create Webmin Group", "Webmin group '$groupname' already exists.");
        } else {
            # Create the group with access to your module
            my $group = {
                'name' => $groupname,
                'modules' => [ 'docker-bedrock' ],
                'members' => [ $username ]
            };
            if (acl::create_group($group)) {
                print_error("Create Webmin Group", "Error creating Webmin group: $group_err");
            } else {
                print_redirect('Success');
            }
        }
    } elsif ($in{'action'} eq 'Set Group to User') {
        my $username = $in{'username'};
        my $groupname = $in{'groupname'};

        # Fetch the users and groups
        my @users = acl::list_users();
        my @groups = acl::list_groups();
        # Find specifics
        my ($group) = grep { $_->{'name'} eq $groupname } @groups;
        my ($user) = grep { $_->{'name'} eq $username } @users;
        # Check was found
        if (!$user || !$group) {
            print_error("Set Group to User", "User '$username' OR Group '$groupname' does not exist. Found User '$user' or Group '$group'.");
        } else {
            # Add user to the group
            $group->{'members'} = [ $username ];
            if (acl::modify_group($groupname, $group)) {
                print_error("Set Group to User", "Error setting group to user: $user_err");
            } else {
                print_redirect('Success');
            }
        }
    }

    print_error("FATAL ERROR!");
} else {
    print_error("NOT ADMIN!");
}
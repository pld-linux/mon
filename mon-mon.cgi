#!/usr/bin/perl

# ----------------------------------------------------------------------
# Web interface for Mon.
# Arthur K. Chan <artchan@althem.com>
#   Based on the Mon program by Jim Trocki <trockij@transmeta.com>. 
#   http://www.kernel.org/software/mon/
# ----------------------------------------------------------------------
# $Id$
# ----------------------------------------------------------------------

# Instructions ---------------------------------------------------------
# 
# Install this cgi script to whereever your cgi-bin directory sits
# on your mon server. If you don't have a web server installed, try
# http://www.apache.org.
# 
# Modify the "Configurable Parameters" section below to customize it
# to your site's settings. Send comment about this web interface to
# Art Chan at the address above.
#
# This script will require the CGI perl module. Available at any
# perl CPAN site. See http://www.perl.org for details.


# Configurable Parameters ----------------------------------------------

$organization = "";				# Organization name.
$monadmin = "";					# Your e-mail address.
$logo = "";					# Company or mon logo.
$reload="180";					# Seconds for page reload.
$monhost="monhost";				# Mon server hostname.
$BGCOLOR = "white";				# Background color
$BUTTONCOLOR = "tan";				# Button bar color

# You shouldn't need to change these.
$url = $ENV{SCRIPT_NAME};			# URL of this script.

# General Declarations -------------------------------------------------

use CGI;				       # Use the cgi module.
use Mon::Client;			       # mon client interface

%OPSTAT = %Mon::Client::OPSTAT;

$webpage = new CGI;			       # Declare instance of mod.

$time = time;				       # This will be used for 
$localtime = localtime(time);		       # the time on the page.


# Reverse sort ---------------------------------------------------------
sub backwards {
    $b cmp $a;
}

# Return untainted host or group name if safe, undef otherwise ---------
sub validate_name {
    return $_[0] =~ /^([\w.\-_]+)$/ ? $1 : undef;
}


# Setup the html doc headers and such ----------------------------------
sub setup_page {
    my ($title) = @_;
    print $webpage->header;
    print $webpage->start_html(-title=>"MON - $title",
                             -BGCOLOR=>$BGCOLOR);
    print $webpage->h1("MON $title");
    if ($logo){
	$webpage->print("\n<img src=\"$logo\"><br><br>\n");
    }
    if ($organization){
	print $webpage->h3("$organization");
    }
    &print_bar;

    $qtime = time;
    @time = localtime($qtime);
    my $ttime = sprintf ("%.2d:%.2d:%.2d", $time[2],$time[1],$time[0]);
    print $webpage->center
	("\nThis information was presented at: $ttime. ");
} 


# Print the button bar -------------------------------------------------
sub print_bar {
    $button = "INPUT TYPE=\"submit\" NAME=\"command\"";
    $webpage->print("\n\n<FORM METHOD=\"GET\">\n");
    $webpage->print("<table bgcolor=$BUTTONCOLOR width=75% border=1 align=center>\n");
    $webpage->print("<tr>\n");
    $webpage->print("\t<td width=3 align=center>Show Operation Status</td>\n");
    $webpage->print("\t<td width=3 align=center>Show Alert History</td>\n");
    $webpage->print("\t<td width=3 align=center>Disable/Enable monitoring.</td>\n");
    $webpage->print("\t<td width=3 align=center>List Disabled Hosts</td>\n");
    $webpage->print("\t<td width=3 align=center>List PIDs for mon processes.</td>\n");
    $webpage->print("\t<td width=3 align=center>Restart Mon</td>\n");
    $webpage->print("</tr>\n");
    $webpage->print("\t<tr><td width=3 align=center><$button VALUE=\"opstatus\"></td>\n");
    $webpage->print("\t<td width=3 align=center><$button VALUE=\"alerthist\"></td>\n");
    $webpage->print("\t<td width=3 align=center><$button VALUE=\"disable\"></td>\n");
    $webpage->print("\t<td width=3 align=center><$button VALUE=\"disabled\"></td>\n");
    $webpage->print("\t<td width=3 align=center><$button VALUE=\"pids\"></td>\n");
    $webpage->print("\t<td width=3 align=center><$button VALUE=\"reset\"></td>\n");
    $webpage->print("</tr></table>");

    $webpage->print("</form>\n");
}


# query the server operational status ----------------------------------
sub query_opstatus {

    print $webpage->center
	("This page will reload every $reload seconds.<br><br>\n");
    $webpage->print("\n<META HTTP-EQUIV=\"Refresh\"");
    $webpage->print("CONTENT=\"$reload\", URL=\"$url\">\n");

    my $c = new Mon::Client (
    	host => $monhost,
    );

    $c->connect();

    if ($c->error ne "") {
    	# ignore the error for now :(
    }

    my %op = $c->list_opstatus();

    if ($c->error ne "") {
    	# ignore the error for now :(
    }

    $c->disconnect();

    $webpage->print("<table align=center border=1 width=35%>");
    $webpage->print
	("<tr><td><font color=black>Service color legend:</font></td>\n");
    $webpage->print("<td><font color=black>Unchecked</font></td>\n");
    $webpage->print("<td><font color=green>Good</font></td>\n ");
    $webpage->print("<td><font color=red>Error</font></td></tr>\n");
    $webpage->print("</table>");    

    $webpage->print
	("<table align=center width=80% border=1>\n");
    $webpage->print
	("<tr><th>Host Group</th><th>Service</th>\n");
    $webpage->print
	("<th>Last Checked</th><th>Est. Next Check</th></tr>\n");

    foreach my $group (sort keys %op) {
	foreach my $service (sort keys %{$op{$group}}) {

	    my $s = \%{$op{$group}->{$service}};

	    $webpage->print("<tr><td>\n");
	    $webpage->print
		("<a href=\"$url?command=group&args=$group\">");
	    $webpage->print("$group</a></td>\n");

	    if ($s->{"opstatus"} == $OPSTAT{"untested"}) {
		$webpage->print("<td><font color=black>\n");
		$webpage->print("$service</font></td>");

	    } elsif ($s->{"opstatus"} == $OPSTAT{"fail"}) {
		$webpage->print("<td><blink>");
		$webpage->print
		    ("<a href=\"$url?command=alert&args=$group,$service\">");
		$webpage->print
		    ("<font color=red>$service</font></a></blink></td>\n");

	    } elsif ($s->{"opstatus"} == $OPSTAT{"ok"}) {
		$webpage->print("<td><font color=green>");
		$webpage->print("$service</font></td>\n");

	    } else {
		my $txt = "";
		for (keys %OPSTAT) {
		    $txt = $_ if ($s->{"opstatus"} == $OPSTAT{$_});
		}
		$webpage->print("<td><font color=purple>");
		$webpage->print("$service ($txt)</font></td>\n");
	    }

	    if ($s->{"opstatus"} == $OPSTAT{"untested"}) {
		$webpage->print("<td>-</td>");

	    } else {
		my @time = localtime ($s->{"last_check"});
		$webpage->print(
		    sprintf ("<td>%.2d:%.2d:%.2d</td>\n", @time[2, 1, 0])
		);
	    }

	    my @time = localtime ($qtime+$s->{"next"});
	    $webpage->print(
		sprintf ("<td>%.2d:%.2d:%.2d</td>\n", @time[2, 1, 0])
	    );
	    $webpage->print("</tr>");
	}
    }
    $webpage->print("</table>\n");    
}


# Extract the list of hosts associated with the group ---------------
sub query_group {

    my $group = &validate_name ($args);

    if (!defined $group) {
	$webpage->print("Invalid host group\n");

    } else {
	my $c = new Mon::Client (
	    host => $monhost,
	);

	$c->connect();

	if ($c->error ne "") {
		# ignore error for now
	}

	@hosts = $c->list_group ($group);

	if ($c->error ne "") {
	    my $e = $c->error;
	    $webpage->print (<<"EOF"
<pre>
Could not list groups: $e
</pre>
EOF
	    );
	    return undef;
	}

	$c->disconnect();

	$webpage->print("<table align=center width=50% border=1>");
	$webpage->print("<th>Members of group \"<em>$group</em>\".</th>") ;    

	foreach my $host (sort @hosts) {
	    $webpage->print("<tr><td>$host</td></tr>") ;
	}
	$webpage->print("</table>");
    }
}


# End the document -----------------------------------------------------
sub end_page {
    &print_bar;
    if ($monadmin) {
	print $webpage->center("For questions about this server. Contact:");
	print $webpage->center
	    ("<a href=\"mailto:$monadmin\">$monadmin</a><br>");
    }
    print $webpage->end_html;
}


# Get the params from the form -----------------------------------------
sub get_params {
    $command = $webpage->param('command');
    $args = $webpage->param('args');
    $enable_host = $webpage->param('enablehost');
    $enable_group = $webpage->param('enablegroup');
    $enable_service = $webpage->param('enableservice');
    $enable_watch = $webpage->param('enablewatch');

    $disable_host = $webpage->param('disablehost');
    $disable_group = $webpage->param('disablegroup');
    $disable_service = $webpage->param('disableservice');
    $disable_watch = $webpage->param('disablewatch');
}


# What to do if the view alert details is depressed --------------------
sub alert {
    local ($arg) = @_;

    my ($group, $service) = split (/\,/, $arg);

    print $webpage->hr;
    $webpage->print
	("<h2>Failure detail for group <font color=red>$group</font> ");
    $webpage->print
	("and service <i>$service</i> test:</h2>");

    my $c = new Mon::Client (
    	host => $monhost,
    );

    $c->connect();

    if ($c->error ne "") {
    	# ignore errors for now
    }

    my %op = $c->list_opstatus();

    if ($c->error ne "") {
    	# ignore errors for now
    }

    $c->disconnect();

    foreach my $g (keys %op) {
	next if ($g ne $group);
    	foreach my $s (keys %{$op{$g}}) {
	    next if ($s ne $service);
	    $webpage->print("$op{$g}->{$s}->{last_summary}\n");
	}
    }

    print $webpage->hr;
}


# List alert history --------------------------------------------------
sub alerthist {
    print $webpage->hr;
    print $webpage->h2("Alert History:");

    my $c = new Mon::Client (
    	host => $monhost,
    );

    $c->connect();

    if ($c->error ne "") {
    	# ignore error
    }

    my @l = $c->list_alerthist();

    $c->disconnect();

    $webpage->print("<table border=1 width=80% align=center>\n");

    $webpage->print("<tr><th>Group</th><th>Service</th>\n");
    $webpage->print("<th>Type</th><th>Time</th><th>Alert</th>\n");
    $webpage->print("<th>Args</th><th>Summary</th>\n");
    $webpage->print("</tr>\n");	

    foreach my $line (reverse sort {$a->{"time"} <=> $b->{"time"}} (@l)) {
	my $localtime = localtime ($line->{"time"});

	$webpage->print("<tr><td><a href=\"$url?command=group&");
	$webpage->print("args=$line->{group}\">$line->{group}</a></td>");

        $webpage->print("<td>$line->{service}</td>\n");
	$webpage->print("<td>$line->{type}</td>\n");
	$webpage->print("<td>$localtime</td>\n");

	$line->{"alert"} =~ s{^.*\/([^/]*)$}{$1};

	$webpage->print("<td>$line->{alert}</td>\n");

	my $args = "-";
	if ($line->{"args"} !~ /^\s*$/) {
	    $args = $line->{"args"};
	}

	$webpage->print("<td>$args</td>\n");
	$webpage->print("<td>$line->{summary}</td>");

	$webpage->print("</tr>\n");
    }

    $webpage->print("</table>\n");	
    print $webpage->hr;    
}


# Generic button function ---------------------------------------------
sub button {
    local ($title, $command) = @_;

    print $webpage->hr;
    print $webpage->h2("$title");
    print "(command not implemented in this client)\n";
    print $webpage->hr;
}


# Form to get item to disable -------------------------------------------
sub disable {
    print $webpage->hr;
    print $webpage->h2("$title");

    $webpage->print ("(command not implemented in this client)\n");

    print $webpage->hr;

    return;

    my ($desc, $cmd, @arg);
    if ($disable_host) {
	$desc = "Attempting to disable a host";
	$cmd = "disable host";
	push @arg, $disable_host;
    } elsif (($disable_group) && ($disable_service)) {
	$desc = "Attempting to disable a service";
    	$cmd = "disable service";
	push @arg, $disable_group, $disable_service;
    } elsif ($disable_watch) {
	$desc = "Disable a watch";
    	$cmd = "disable watch";
	push @arg, $disable_watch;
    } elsif ($enable_host) {
	$desc = "Attempting to enable a host";
	$cmd = "enable host";
	push @arg, $enable_host;
    } elsif (($enable_group) && ($enable_service)) {
	$desc = "Attempting to enable a service";
	$cmd = "enable service";
	push @arg, $enable_group, $enable_service;
    } elsif ($enable_watch) {
	$desc = "Enable a watch";
	$cmd = "enable watch";
	push @arg, $enable_watch;
    }
    if ($desc) {
	my $bad = 0;
	for (@arg) {
	    $_ = &validate_name($_);
	    $bad = 1 if !defined $_;
	}
	if ($bad) {
	    # Don't try to print out the invalid arg, it wouldn't be
	    # safe.
	    print "Invalid argument for $cmd.\n";
	}
	else {
	    print "$desc: @arg<br>\n";
	    for (@arg) {
		$cmd .= " \Q$_";
	    }
	    open (MON, "$moncmd -s $monhost $cmd|");
	    while (<MON>) {
		print "$_<BR>\n";
	    }
	    close MON;
	}
	print $webpage->hr;
    }

    print "<table width=100%>";
    print "<tr><td>";
    print $webpage->startform(GET);
    print "Disable a host.<br>\n";
    print $webpage->textfield('disablehost');
    print " Hostname<br>";
    print $webpage->submit(-name=>'command',-value=>'disable');
    print $webpage->endform;
    print "</td><td>";
    print $webpage->startform(GET);
    print "Enable a host.<br>\n";
    print $webpage->textfield('enablehost');
    print " Hostname<br>";
    print $webpage->submit(-name=>'command',-value=>'enable');
    print $webpage->endform;
    print "</td></table>";
    print $webpage->hr;

    print "<table width=100%>";
    print "<tr><td>";
    print $webpage->startform(GET);
    print "Disable a service for a group.<br>\n";
    print $webpage->textfield('disablegroup');
    print " Group<br>";
    print $webpage->textfield('disableservice');
    print " Service<br>";
    print $webpage->submit(-name=>'command',-value=>'disable');
    print $webpage->endform;
    print "</td><td>";
    print $webpage->startform(GET);
    print "Enable a service for a group.<br>\n";
    print $webpage->textfield('enablegroup');
    print " Group<br>";
    print $webpage->textfield('enableservice');
    print " Service<br>";
    print $webpage->submit(-name=>'command',-value=>'enable');
    print $webpage->endform;
    print "</td></table>";
    print $webpage->hr;

    print "<table width=100%>";
    print "<tr><td>";
    print $webpage->startform(GET);
    print "Disable a watch.<br>\n";
    print $webpage->textfield('disablewatch');
    print " Watch<br>";
    print $webpage->submit(-name=>'command',-value=>'disable');
    print $webpage->endform;
    print "</td><td>";
    print $webpage->startform(GET);
    print "Enable a watch.<br>\n";
    print $webpage->textfield('enablewatch');
    print " Watch<br>";
    print $webpage->submit(-name=>'command',-value=>'enable');
    print $webpage->endform;
    print "</td></table>";
    print $webpage->hr;
}



# Main program ---------------------------------------------------------

&get_params;				       # Read the args.

if ($command =~ "group" ){		       # Expand hostgroup.
    &setup_page("Group Expansion");
    &query_group;
}
elsif ($command =~ "alerthist"){	       # Alert history button.
    &setup_page("List the alert history");
    &alerthist;
}
elsif ($command =~ "alert"){		       # View alert details.
    &setup_page("Alert Details");
    &alert($args);
}
elsif ($command =~ "disabled"){		       # Disabled hosts button.
    &setup_page("List disabled hosts");
    &button("Disabled hosts:","list disabled");
}
elsif ($command =~ "disable"){		       # Disabled 
    &setup_page("Disable/Enable alert for host, group. or service");
    &disable;
}
elsif ($command =~ "enable"){		       # Disabled 
    &setup_page("Disable/Enable alert for host, group. or service");
    &disable;
}
elsif ($command =~ "pids"){		       # View pid button.
    &setup_page("List pids of server, alerts and monitors.");
    &button("List pids for all mon processes:", "list pids");
}
elsif ($command =~ "reset"){		       # Reset mon button.
    &setup_page("Restart Mon.");
    &button("Attempting to reset mon...","reset");
}
# Button "opstatus" will fall through to else.
else {					       # All else.
    &setup_page("Operation Status");
    &query_opstatus;
}

&end_page;


# That's it! ----------------------------------------------------

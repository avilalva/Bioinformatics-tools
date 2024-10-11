#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

# Create a new CGI object
my $cgi = CGI->new;

# Check if the user has uploaded files
if ($cgi->request_method eq 'POST') {
    my $ensembl_list_file = $cgi->upload('ensembl_ids');
    my $fasta_file = $cgi->upload('fasta_file');
    
    # Handle missing files
    unless ($ensembl_list_file && $fasta_file) {
        print $cgi->header(-type => 'text/html');
        print $cgi->start_html(-title => 'FASTA Sequence Checker');
        print "<div style='text-align: center; padding-top: 50px;'>";
        print $cgi->h2("Error: Missing Ensembl ID list or FASTA file.");
        print "</div>";
        print $cgi->end_html;
        exit;
    }

    # Read Ensembl ID list
    my @ensembl_ids = <$ensembl_list_file>;
    chomp @ensembl_ids;
    close($ensembl_list_file);

    # Read FASTA file and collect headers
    my %fasta_headers;
    while (my $line = <$fasta_file>) {
        chomp $line;
        if ($line =~ /^>(\S+)/) {  # Match FASTA headers (first word after '>')
            my $ensembl_id = $1;
            $fasta_headers{$ensembl_id} = 1;  # Store header ID
        }
    }
    close($fasta_file);

    # Output the results in HTML table format
    print $cgi->header(-type => 'text/html');
    print $cgi->start_html(-title => 'FASTA Sequence Checker', -style => { -code => '
        body { text-align: center; padding-top: 50px; }
        table { margin: 0 auto; border-collapse: collapse; width: 50%; }
        th, td { padding: 10px; border: 1px solid #ddd; }
        .yes { background-color: #d4edda; color: #155724; }
        .no { background-color: #f8d7da; color: #721c24; }
    '});
    
    print "<h1>FASTA Sequence Checker</h1>";
    print "<p>Below is the status of each Ensembl ID:</p>";
    print "<table>";
    print "<tr><th>Ensembl ID</th><th>Present</th></tr>";

    # Loop through Ensembl IDs and check if they're in the FASTA headers
    foreach my $id (@ensembl_ids) {
        my $status = $fasta_headers{$id} ? "<td class='yes'>Yes</td>" : "<td class='no'>No</td>";
        print "<tr><td>$id</td>$status</tr>";
    }

    print "</table>";
    print $cgi->end_html;

    exit;
}

# Display the HTML form if no POST request
print $cgi->header(-type => 'text/html');
print $cgi->start_html(
    -title => 'FASTA Sequence Checker',
    -head => [ $cgi->meta({-charset => 'UTF-8'}) ]
);

# Centered form with logo
print "<div style='text-align: center; padding-top: 50px;'>";

# Add a space for the logo
print "<img src='http://localhost/seqchek.png' alt='Logo' style='max-width: 500px; margin-bottom: 20px;'>";  # Replace with actual logo path

# Form title
print "<h1>FASTA Sequence Checker</h1>";
print "<p>Please upload a list of Ensembl IDs and a FASTA file to check for the presence of sequences.</p>";

# Display the form
print $cgi->start_form(
    -method => 'POST',
    -enctype => 'multipart/form-data'
);
print $cgi->filefield(-name => 'ensembl_ids', -size => 50), "<br><br>";
print $cgi->filefield(-name => 'fasta_file', -size => 50), "<br><br>";
print $cgi->submit(-value => 'Submit');
print $cgi->end_form;

print "</div>";
print $cgi->end_html;

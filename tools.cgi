#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

# Print the HTML header
print header();
print start_html(
    -title  => 'Bioinformatics Tools',
    -style  => {-src => 'https://example.com/style.css'}  # Optional: change this to your own CSS if needed
);

# Create a centered div for the content
print "<div style='text-align: center; padding-top: 50px;'>";

# Header title
print "<h1>Bioinformatics Tools</h1>";

# Add tool links
print "<ul style='list-style-type: none; font-size: 20px;'>";

# Add links to the scripts
print "<li><a href='/cgi-bin/charcount.cgi'>1. FASTA Character Count Tool</a></li><br>";
print "<li><a href='/cgi-bin/fastaseqcount.cgi'>2. FASTA Sequence Count Tool</a></li><br>";
print "<li><a href='/cgi-bin/fastapositionextract.cgi'>3. FASTA Position Extract Tool</a></li><br>";
print "<li><a href='/cgi-bin/cgcontent.cgi'>4. CG Count Tool</a></li><br> ";
print "<li><a href= '/cgi-bin/seqchecker.cgi'>5. Sequence Checker</a></li><br>";
print "</ul>";

# End of content div
print "</div>";

# End the HTML
print end_html();

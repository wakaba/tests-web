use strict;

package mixed_replace_generation;

sub new ($;%) {
  my ($class, %opt) = @_;
  return bless {boundary => 'abcdefghijklmn', out => \*main::STDOUT,
      nl => "\x0D\x0A", %opt}, $class;
} # new

sub output_cgi_header ($) {
  my $self = shift;
  print {$self->{out}} q<Content-Type: multipart/x-mixed-replace; boundary=">
      . $self->{boundary} . qq<"\n>;
  print "\n";
} # output_cgi_header

sub output_line ($$) {
  my ($self, $s) = @_;
  print {$self->{out}} $s . $self->{nl};
} # output_line

sub output_string ($$) {
  my ($self, $s) = @_;
  print {$self->{out}} $s;
} # output_string

sub output_boundary ($) {
  my $self = shift;
  print {$self->{out}} $self->{nl} . '--' . $self->{boundary} . $self->{nl};
} # output_boundary

sub output_last_boundary ($) {
  my $self = shift;
  print {$self->{out}}
      $self->{nl} . '--' . $self->{boundary} . '--' . $self->{nl};
} # output_last_boundary

1;

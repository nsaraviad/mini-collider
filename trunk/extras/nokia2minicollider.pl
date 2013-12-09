#/usr/bin/perl -w
use strict;

my $start_c = 11;

my %notes = (
 'c'  => 0,
 'c#' => 1,
 'd'  => 2,
 'd#' => 3,
 'e'  => 4,
 'f'  => 5,
 'f#' => 6,
 'g'  => 7,
 'g#' => 8,
 'a'  => 9,
 'a#' => 10,
 'b'  => 11,
);


sub get_note {
	my ($note, $tempo, $oct) = @_;

	my $tune = $notes{$note} + ($oct - 1) * 12;
	$tempo = 32 / $tempo;
	
	return "{-1;1}.loop($start_c).expand.tune($tune).loop($tempo)";
}

sub get_silence {
	my ($tempo) = @_;

	$tempo = 32 / $tempo;
	
	return "silence.loop($tempo)";
}

sub get_minicollider_code {
	my @tab_notes = @_;

	my @cnotes;
	foreach my $tnote (@tab_notes) {
		my $cnote;

		if ($tnote =~ m/^(\d+)([a-g]#?)(\d)$/) {
			$cnote = get_note($2, $1, $3);

		} elsif ($tnote =~ m/^(\d+)\.([a-g]#?)(\d)$/) {
			$cnote = get_note($2, $1 + 0.5, $3);

		} elsif ($tnote =~ m/^(\d+)#?([a-g])(\d)$/) {
			$cnote = get_note("$2#", $1, $3);

		} elsif ($tnote =~ m/^(\d+)\.#?([a-g])(\d)$/) {
			$cnote = get_note("$2#", $1 + 0.5, $3);

		} elsif ($tnote =~ m/^(\d+)-/) {
			$cnote = get_silence($1);

		} else {
			die "Nota incorrecta: $tnote";
		}

		push @cnotes, $cnote;
	}

	return  "{\n" . join(";\n", @cnotes) . "\n}.play\n";
}

my $tab = <>;
my @tab_notes = split(/\s+/, $tab);
print get_minicollider_code(@tab_notes);
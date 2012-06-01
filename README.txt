A Semantic Web Viewer / Editor built using Python

I'm planning to build a Semantic Web Viewer/Editor similar to Tabulator / Marbles / Disco etc. I've set out a (rather ambitious) plan below.

Command Line:
	View Triples on command line

HTML Semantic Web Viewer:
	View all triples given at a URI as a table (using query string)
	Upgrade subject to <h1>
	make URIs links - (note hash uris will have to be urlencoded %23)
	Display rdfs:label if possible rather than uri (may have to dereference and cache uris)
	Display map/image if possible rather than uri


HTML Semantic Web Editor:
	Add form to add a triple
	Add forms to add an object for each predicate or add a predicate at the end
	Use appropriate form widgets
	Search for appropriate objects by label (like a non-AJAX Autosuggest)
	Allow adding new objects

Javascript / AJAX:
	Validation
	Autosuggest for object properties

Versioning:
	Provenance: User, Timestamp

Authorisation:
	Rules Grant/Deny - Read/Write/Delete Access

Preferences:
	What Information to Show (ie. what's irrelevant / poor sources)

Clinical Decision Support:
	Deterministic
		Heristics
		Guidelines

	Probabalistic
		Coding Clinical Trials
		Statistics from Self
		Machine Learning
		Automatically Generating Trials

I plan to start out using python, django, rdflib, aptana, pydev, github. 


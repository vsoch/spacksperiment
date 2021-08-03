# Titles

For this experiment, we want to test different strategies for discovering
packages in issue titles. This means we will:

1. Download compete issue metadata for spack
2. Test scripts against it.

The discussion / idea started [here](https://github.com/spack/spack-bot/pull/28#discussion_r681256500)
and specifically we want to test this approach for finding a package:

1. get updated list of packages from [here](https://spack.github.io/packages/data/packages.json)
2. create a simple regular expression to search for names
3. do the search in the title

## Usage

Export a GitHub token to the environment.

```bash
$ export GITHUB_TOKEN=xxxxxxxxxxxxxx
```

Run the following script to dump issues into [data](data):

```bash
$ python get-issues.py
```

And then run the script to parse them.

```bash
$ python parse-issues.py
```

The output files of interest are [matches.json](matches.json) with found matches,
and [misses.json](misses.json) with titles that weren't matched. I think we can clearly
see that we need to remove special characters so a pattern like `package: thing` is matched.

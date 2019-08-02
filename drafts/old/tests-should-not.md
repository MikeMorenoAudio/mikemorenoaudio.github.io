# Tests should not...

## Have a liberal use of fixture files  

<small>A fixture file is a file with static data in it, it's often used as a file representation of a row in a database.</small>

### Why?

A fixture file shared among tests is global data and is no different to assigning global variables all over the place.
The worst thing about tests that use a fixture file is that changing the file for one test could break it for another.

## Have multiple assertions in a test

### Why?

If a test has multiple assertions, it also has multiple reasons to fail. A test should fail for one purpose and one purpose only.

### Example

```
bad test here
```

```
good test here
```

## Hit real things (unit tests only)

### Why?

Your database and its data change. If the data changes in such a way that it breaks your test, you have a flaky test.
The solution here is to use mock objects where you can. Doing so will allow you to force a specific response from
whatever function it is you're calling.

```
Bad test here
```

```
good test here
```



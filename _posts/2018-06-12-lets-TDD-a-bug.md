---
layout: default
tags: programming
---

# TDD'ing bugs

I've recently started writing a CLI in Typescript to detect dead css,
it's called [Mort](https://github.com/joereynolds/mort).

![A gif demonstrating mort](/assets/mort.gif)

## The bug

There was a bug that has existed since it's early days as a [shell script](https://github.com/joereynolds/configs/blob/master/dotfiles/bash/.bashrc#L30).

I found out the cause of the bug by chance, thanks to Vim echoing a helpful `[dos]` when I saved the troublesome file.
The bug was caused by Windows-style line-endings in CSS files (story of my life...), the output would be garbled and malformed.

On Unix files it looks like this:
```
: mort assets/css/main.css
0 usages found, menu active, can probably be removed.
0 usages found, text ul, can probably be removed.
0 usages found, text ol can probably be removed.
0 usages found, article + article can probably be removed.
```

But on Windows files, it looked like this:
```
: mort assets/css/main.css
 can probably be removed.ve,
 can probably be removed.
 can probably be removed.
 can probably be removed.
 can probably be removed. article
 can probably be removed.ag
```

Let's fix the bug the "TDD way".

- Write a test to confirm the bug has been fixed.
- Fix the bug.

# Write your assertions first

Before you write any actual code, write a test case to confirm the bug is fixed (or, will be fixed).

```
// Bug fix:
// https://github.com/joereynolds/mort/issues/6
test("It can handle unix and windows line endings", () => {
    const expected = [
        ".menu .active",
        ".hljs{",
        ".text ul,",
        ".text ol {",
        ".song {",
        ".article + .article",
        ".article-tag",
    ];
    const selectors = new Selectors();
    expect(selectors.fromFile("test/bug-fixes/windows-line-endings.css")).toEqual(expected);
});
```

Once we have the test case set up, we can then go about starting to write the code to fix the bug.
In my case, it was fairly simple, split on `\n` for Unix, and `\r\n` for Windows.

**Before**

```
const selectors = fileContents.split("\n").filter(selector => {
```

**After**

```
const selectors = fileContents.split(/(\r\n|\n)/g).filter(selector => {
```

Once you've written the code to fix the bug, run the tests (`npm test`) and they should pass.

![A passing test suite for mort](/assets/mort-test.png)
And that's it!

We've fixed the bug and we have a method of proving it whenever we want. This will help 
reduce regressions with any future releases :)

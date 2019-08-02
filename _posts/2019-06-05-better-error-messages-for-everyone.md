---
layout: default
tags: programming
---

# Better error messages for everyone

An all too common thing for all developers (not just newbies) is vague error
reporting with blanket statements pinpointing you to precisely 0 solutions to
the issue.

Consider the following simple but real example of an error message:

(Note that all the code below is language agnostic and abstracted away. We 
want to focus on the messages, not the implementation.)

```
You do not have enough permissions to perform this request.
```

What's wrong here?

Well, the stack trace will handle telling us what file and line number caused
it,
but with a bit of forethought, we could help the user out even more by providing
*contextual information*.

Contextual information in an error can tell us more about the situation.

We can refactor this error to provide such information as:

- Who doesn't have permissions to perform the request?

- What do they need to do to be able to perform the request?

- Why can't they perform the request?

Once we've answered those 3 questions, we end up with an error looking like this

```
                                 Who          What                                    Why  
                                  |            |                                       |
To perform this request, the user %s needs the %s permissions. They currently have the %s permissions.
```

With the above, you've given the user enough information to debug and fix things
on their own. You've informed them of the problem and now it's their issue to
fix. 

Then again, it's all well and good for me to assume you have all the knowledge of what went
wrong available to you, so let's go through some code examples with some less
than ideal scenarios.

Before we go on to real life scenarios, let me quickly talk about something
worse than a bad error message, no error message.

## Hiding error messages

Hiding error messages is something that developers tend to do and they continue
to take this practice with them throughout their software career and to their
graves.

Here's an example of hiding a message in Python:

```
try:
    do_something()
except Exception:
    pass
```

There are many things wrong with this, so let's discuss them.

First off, just `pass`ing on the exception is a terrible idea. You will never
see the exception and it will fade away into the ether for no one to realise.

Let's rework it:

```
try:
    do_something()
except Exception as e:
    print("Failed to do_something(): " + str(e))
```

This is slightly better, at least now we're seeing that something is wrong.

There's still some bad practice in here though, you're catching `Exception`. 
In Python, this is the 'catch all'
exception. It's good practice to be specific when it comes to errors because we
should (in theory) know what's going to go wrong with our program in a worst
case scenario.

Let's rework that once more:

```
try:
    do_something()
except DoSomethingDidntDoSomethingException as e:
    print("Failed to do_something(): " + str(e))
```

Now that we've got our specific error reporting out, we *should* add a
catch all case for anything else that *could* happen. Our final result is this:

```
try:
    do_something()
except DoSomethingDidntDoSomethingException as e:
    print("Failed to do_something(): " + str(e))
except Exception as e:
    print("Failed to do_something() in a very bad way: " + str(e))
```

With that out of the way, let's get back to the real world examples and how to
improve them.

## Real life examples

## 1

Our first example is a tricky one. We don't actually throw or catch any
exceptions so we can hardly catch or explain the problem in an elegant way, unless we
refactor the code. 

```
public function handle()
{
    $model = App::make($this->location . studly_case($this->argument('model')));

    $this->info(
        $model->run($this->argument('keep-days')) ?  "Table(s) pruned": "Something went wrong"
    );
}
```

The best we can hope to achieve with this amount of information is maybe just a
slight rewording and hinting at what was happening:

```
public function handle()
{
    $model = App::make($this->location . studly_case($this->argument('model')));
    $errorMessage = "There was an error pruning tables"

    $this->info(
        $model->run($this->argument('keep-days')) ?  "Table(s) pruned": $errorMessage
    );
}
```

True, it's not that much better but at least now if we see this output, we know
where it's come from. Still, If the code had thrown exceptions in the first
place we could catch and report on this properly.

## 2

Our next example gives us more to work with. 

```
class UserAlreadyUnlockedException
{
    protected $error = 'This user is already unlocked.';
}
```

This jumps out straight away. If you saw this message, you'd be wondering to
yourself "Okay, which user?", so let's answer that for them.

```
class UserAlreadyUnlockedException
{
    protected $error = 'The user %s is already unlocked.';
}
```

Again, quite a simple message with not much going on. Still, we've
managed to give some information to the user and they can go away and do what
they need to with it.

## 3

Going right back to the start of this article, we had the below:

```
class PermissionDeniedException
{
    protected $error = 'You do not have enough permissions to perform this request.';
}
```

This error is rife with opportunity to supply more information:

```
class PermissionDeniedException
{
    protected $error = 'To perform this request, the user %s needs the %s permissions. They currently have the %s permissions.';
}
```

The only issues here are practical ones. Giving them all of this data relies on
us *retrieving* all of this data (The groups the user's in, the groups the user needs to be in, and the
username) from somewhere. 

All this retrieval of data bares one obvious and disheartening side-effect,
heavier code.

Leading to our next point...

## User Experience beats your ego

I've fallen into this trap before. Being hesitant to 'clog' up the code because
I don't want to sully my work for the sake of better errors (which seemed
unimportant to me at the time).

All I can say is you need to drop your ego off at the door and remember why
you're writing that code in the first place. Users use your code,
not you. You code for them, write better exceptions/logs for them too.

An instance of my preaching can be found in one of my projects, [mort](https://github.com/joereynolds/mort). `mort` was my first dive into a proper CLI and also my first look at Typescript. 

It logs all over the place and very verbosely, it features the following logging:

- 3 different verbosity levels, 
    - `-v` (display the file being operated on), 
    - `-vv` (displays level 1 + the command generated by `mort`)
    - `vvv`  (displays levels 1 + 2 + displays all of the searches it's
      performing.)

- A message on failure of opening a file, and the name of the file.

- A warning emitted when a user does not have a program installed (and a
  subsequent warning to let the user know we have found and are using an
  alternative).

If you have some common sense and start putting yourself in the user's shoes,
you'll find your error messages improve. Remember that during
development, it's likely that you're the person that's going to be encountering these
messages and wishing they made more sense, so do yourself a favour.

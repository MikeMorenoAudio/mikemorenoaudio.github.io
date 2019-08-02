# Hunspell and Aspell

In work I can use `hunspell` to look through all of our Email templates and scan
for typos (I spotted some manually the same day I found hunspell.). 


## Hunspell

```
hunspell -l *.html
```

## Aspell

```
cat *.html | aspell list
```


I like to make the output a bit nicer and less duplicated though        

```
hunspell -l *.html | sort -u
```

Finally, after a bit of bending it to my will, we end up with this

```
hunspell -l *.html | sort -u | xargs -L1 rg
```

This'll grep for all of the typos that we've just found and show us where they
are. This can then be piped into Vim's quickfix list or whatever else you want
to do but I feel like I've shown you enough pipes for now.

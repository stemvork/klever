# klever

## Notes
0. basic scene
1. field objects are white rects attached to a layer, grouped
2. die needs to be thrown, drawn and grouped (no dots)
3. define some _pretty_ distinguishable colors
4. press space to test new turn/throwing dice again
5. die needs to have dots drawn
6. always add tuples
7. label for green fields in top margin
8. labels for oranges fields in squares
9. less than sign polygons for purple fields
10. click a die to play it to a field
11. determine desired interactions through state
12. put the value into the field if purple or orange
13. return false if invalid move
14. put an X in the field if green
15. labels for green field requirements
16. larger cross, but also remove the label behind it
17. need to keep track of req labels
18. change from dice to groups of values, rects and dots
19. get the bound union of all the dice bounds
20. allow the making of empty dice object
21. use add and take for moving to dice or to silver
22. include the color index in the tuple
23. the field object also keeps its own scores # TODO: move
24.  colored square behind white square, try to move labels away
25.  separately draw green margin
26.  function to write green labels
27.  proto square function to separate some logic
28.  function to write oranges labels
29.  function to write purples less than signs
30.  move these color specific checks in play and cross out of field class
31.  in fact, contain color-value-rect-dots in one object
32.  draws rect and dots to layer
33.  in fact, change to list of Die instances
34.  draw silver plate and its dice in the newer fashion
35.  write the bound union function in the newer fashion
36.  rewrite the die class to fit the following usage
37.  arrange the dice in a smart way
38.  getters and setters for color and value
39.  proto function for adding square
40.  layer index not working #FIXME
41.  throw the die and refresh the sprites

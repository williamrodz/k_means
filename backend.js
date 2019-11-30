document.ajax({
  type: "POST",
  url: "~/k_means.py",
  data: { param: 3}
}).done(function( o ) {
   // do something
});

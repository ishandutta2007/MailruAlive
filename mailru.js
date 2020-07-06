 mailru.events.listen (mailru.connect.events.login, function (session) {
   // this function will be called upon login
   alert (session.ext_perm);  // shows the privileges of the logged in user
 });
 mailru.connect.login (['widget', 'photos']);




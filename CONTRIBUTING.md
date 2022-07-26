# Contributing Guidelines

Welcome everyone to contribute to this repository.

There are a few guidelines you need to follow. 

### Steps of Contributing

1. Fork this repository into your GitHub account.

2. Clone your repository into your computer, and deploy the code to your local machine.

3. When you finish writing your code, push that to your repository.

4. Send a pull request to the ```funny-nation/Funny-Nation``` repository, ```dev``` branch, and wait until your code passes all the CI tests.

5. If your code passed all the tests, leave it to administrators, and they will handle that. 

### Rules

* All the Typescript code must follow the [Standard.js code style](https://standardjs.com/rules.html). 
  * This project contains Eslint; you might need to set it up in your IDE. 
  * Eslint check is included in the continuous integration process. 

* You can only send your pull request to ```dev``` branch.

* Do not commit the files that should be ignored, such as ```.idea``` and ```xxx.log```.

* Use English for all documentations and comments (include your git commit comments).

* Do not use ```xxx.d.ts``` in this project. 

* You must test your code before you send a pull request. 

* You must follow [SOLID rules](https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) (Single-responsibility principle, Open–closed principle, Liskov substitution principle, Interface segregation principle, and Dependency inversion principle). 

* ```Webstorm``` is a recommended IDE for this project. 

* All features must support multi-languages. You must use ```/src/language/``` module for your language management. 

There is more information in [Developer Guides](docs/developer-guides.md); please make sure you read that before coding. 

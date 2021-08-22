# Changelog

## v0.1.0 (2021-08-22)

#### New Features

* show post description in posts list
* added description field to create post and update post
* added description field to post model
* show comment body
* show published date instead of datetime
* privacy policy page
* logout view
* removed state field from update post form
* publish post view
* minor improvements
* admin post detail and update post
* verify subscription email
* subscribe view
* subscription form
* create subscription
* send email to comment author when comment is approved
* added subject to send method
* send email when comment is created
* simple email client
* list pending comments and approve them
* set default value to name in post comment
* show only approved comments
* post comment form and show comments in post detail
* made post title linkable
* show message when username/password are wrong
* post comment view
* added name field to PostComment
* added post comment model
* exclude analytics script if user is authenticated
* filter draft/published posts
* added state field to post
* parse post body
* added createt_at and modified_at to post
* post detail view
* posts view
* added author to post
* create new category if it does not exists
* redirect to next path after login
* create post view
* create post form view
* admin app
* blog app with category and post models
* redirect to root if is authenticated
* create tables on start
* login view
* get login view
* login user
* do not encrypt password when is get from db
* create user with encrypted password
* added things about me
* removed font-awesome css
* serving static files in dev environment
* css optimizations and social media icons
* html and css improvements
* init tailwindcss configuration
* SEO improvements
* added main meta tags
* added linkedin link
* run application with uvicorn
* simple index page
#### Fixes

* changed test name in mailing
* set cookie values
* privacy policy
* Set anonymous name in subscription when name is empty
* redirect to next after login
* paths
* validate email in comment form
* validate email in subscription form
* check if the email was already subscribed
* admin email and added SITE setting
* removed post_id in post comment
* added empty option
* set cookie with right domain
* return 302 status code
* responsive
* mobile version about me
* changed font-awesome url
#### Refactorings

* extract and move method
* public templates inheritance
* created subscription package
* post comment in post detail view
* use include statement
* extract function
* authentication
* settings
* hide password separator
* views doesn't know about models
* project structure
* magic number
* do not encode salt
#### Docs

* version improvements
#### Others

* docker improvements
* improvements
* env in dockerfile
* docker improvements
* get latest
* list
* fixed working directory
* fixed working directory
* removed sudo
* install docker-compose
* pull image from dockerhub
* twitter card and open graph improvements
* updated Readme
* added twitter card and open graph meta tags
* updated todo for version 1
* TODO
* show all complexity with radon
* removed docker stop
* added plausible snippet
* added uvloop to requirements
* install requirements too
* circle ci config
* dockerization
* project structure and boilerplate
* added footer
* body block within main tag
* subcription page
* posts page
* base h2, ul, ol and a tags
* message
* comments section
* post comment form
* post datetime alignment
* initial article styles
* better postition for social media icons
* spy MailClient
* use simple inheritance instead mixin
* create db schema
* realoading nginx

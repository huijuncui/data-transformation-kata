# Data Ingestion Kata

One of our main objectives at Deep Lens is to match patient cancer patients with the best possible clinical trials
available. Doing this, as you can imagine, requires us to ingest and process a large amount of patient data in order to
make the most accurate recommendations possible.

In this kata, you will be tasked with creating a scaled down version of our data ingestion pipeline. You will need to 
consume patient records in two different formats (CSV and XML) and output them in a standardized format (JSON). 

The detailed requirements are as follows. If you have any questions while you're going through the process, please feel
free to reach out!


## Basic Technology Requirements

- You may complete this kata using whatever language or platform you feel best solves the problem.
- The application should have a single entry point and should be easily executed with via command line.
- There are not GUI requirements for the project.

## Ingestion Requirements

- The application will ingest patient files from two locations &mdash; `data/in/xml` and `data/in/csv`. 
- Any given file should only be processed once during each run of your application. It is ok to re-process files on
subsequent runs of the application, however.
- The application can terminate when there are no files left to process.

**XML Format**\
Each XML file contains a data for _a single patient_.

**CSV Format**\
Each CSV file contains data for _multiple patients_. Additionally, the `conditions` columns contains a pipe (`|`)
delimited list of conditions.

## Transformation Requirements

Each _patient record_ should be transformed into a JSON document that matches the following schema.

```json
{
    "mrn": "0000000",
    "firstName": "first",
    "lastName": "last",
    "middleName": "middle",

    "demographics": {
        "dateOfBirth": 315532800,
        "sex": "M"
    },

    "conditions": [
        { "code": "XX.00", "name": "condition" }
    ]
}
```

- Any missing values should result in a `null` value on the final JSON document.
- Dates should be formatted using Unix Epoch timestamps (seconds since Jan 1, 1970).
- Accepted values for a patient's sex are "M" (Male) and "F" (Female).

## Output Requirements

- Each patient JSON document should be written as a file to the local file system.
- The files must be written with the follow `data/out/{timestamp of job}/patient_{mrn}.json`

## Bonus / Future Requirements

The follow requirements do not have to be implemented in your final application. You are more than welcome to include
them in your solution if you choose, but we are interested in discussing _how_ you might approach them when reviewing
your solution with you.

- Each patient JSON document should keep track of the source file it was generated from
(e.g. `"source": "xml/patient3.xml"`)
- The application should run continually a process new files as they are landed in the target location(s). 
- Files should _not_ be reprocessed after the application restarts. 
- Source files can be moved, but not deleted.
- The application should require a patient record to contain a medical record number (`mrn`). Failed documents should be
moved to a failed document directory (e.g. `/data/error/xml/failed.xml`).

## Submitting Your Kata

To submit your work to Deep Lens, please email either a [git bundle](https://git-scm.com/docs/git-bundle) or zip file
of our code. Please include any necessary instructions or requirements for running your code.

## **THANK YOU!**

From everyone at Deep Lens, we'd like to thank you for taking the time to put together your solution. We know we're
asking you to take time away from family, friends, or life in general to put this together. Regardless of the
outcome, that means the world to us. You rock!
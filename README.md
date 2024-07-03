# MLOps in Databricks workshop
This repository is meant as a demo for using MLOps in Databricks by looking at the use case of accurately predicting wine score

Steps to run AutoML experiments and track models with MLFlow:
1. Open your workspace
2. Click on Create -> Git folder
3. Choose Github as provider and paste the repository URL: [https://github.com/jitendraRai/GnAI_Databricks_Proj.git]
4. The first step in data preparation is to setup the database and tables. Go to database_setup and run all cells (make sure to use your own name)
5. Go to Catalog and check if your database and tables are there.
6. Go back to your workspace and open data_preprocessing. Follow the steps in this notebook.
7. Some data preprocessing steps can be improved. We don't have much time to implement these improvements, but can you think of 3 possible improvements to the train and test data?
8. Go back to Catalog and look at your train and test tables' Sample Data. These should now be filled with data!
9. It is now time to run an AutoML experiment using your train data. Go to Experiments -> Create AutoML Experiment.
10. In the Configuration Pane, choose the right ML problem, data, columns and prediction target.
11. Go to advanced and put the Evaluation Metric on Mean-Absolute Error. **Also make sure to set the timeout at 10 minutes.** Finally, start the experiment!
12. Answer the second question
13. After 2-3 minutes, a button to view the data exploration notebook should appear. Click on it and explore the data using the auto=generated notebook and answer question 3 and 4

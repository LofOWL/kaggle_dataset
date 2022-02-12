# 1. (step_1.py) collect notebook name by votecount
    kaggle kernels list --kernel-type 'notebook' --sort-by 'voteCount' 

    # kaggle_notebook_view_count.csv (1100)


    ## 1.1 [pending] (step_1_1.py) collect notebook name by using crawler
        # default is sorted by hotness
        https://www.kaggle.com/code?sortBy=voteCount&page={self.page}
        https://www.kaggle.com/code?page={self.page}
        # target: 10000 notebooks

# 2. (step_2.py) collect number of version for notebook from kaggle_notebook_view_count.csv
    # kaggle_notebook_view_count_versions.csv (1051)
    # name,copy_edit,versions,tags,comments

    ## 2.1 (step_2_1.py) clean up kaggle_notebook_view_count_versions.csv 
    # clean_kaggle_notebook.csv {versions >= 2} (723)
    # error_kaggle_notebook.csv {version} (283)

    ## 2.2 (step_2_2.py) recollect error_kaggle_notebook.csv
    # error_kaggle_notebook_recollect.csv (279)

    ## 2.3 (step_2_3.py) merge error_kaggle_notebook_recollect.csv with clearn_kaggle_ntoebook.csv and filter into final version
    # final_kaggle_notebook.csv (998)


# 3 (step_3.py) collect down the notebooks with more than one versions into txt
    # /media/lofowl/My Passport/kaggle_notebooks (21449)

    # 3.1 (step_3_1.py) convert collect txt (21449) into ipynb
    # /media/lofowl/My Passport/kaggle_notebooks_ipynb ()

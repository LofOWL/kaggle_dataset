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
    # final_kaggle_notebook.csv (997)


# 3 (step_3.py) collect down the notebooks with more than one versions into txt
    # /media/lofowl/My Passport/kaggle_notebooks (19426)

    # 3.1 (step_3_1.py) convert collect txt (19426) into ipynb
    # /media/lofowl/My Passport/kaggle_notebooks_ipynb ()


# n_1 (step_n_1.py) using meta data to find all the url of notebooks
    # https://www.kaggle.com/kaggle/meta-kaggled
    # url_kaggle_notebook.csv (628567)

# n_1_1_1(step_n_1_1_1.py) merge url_kaggle_notebook.csv with Kernels.csv 
    # Kernels_Url.csv (628568)

# n_1_1_2(step_n_1_1_2.py) filter by votes 
    # Filter_Kernels_Votes_Notebooks.csv (209387)

# n_1_1 (step_n_1_1.py) filter out all the notebooks and find the counts
    from #url_kaggle_notebook.csv
    to #Filter_Kernels_Url_Notebooks_Versions.csv (209387)

# n_1_2 (step_n_1_2.py) filter out all the notebooks
    from #kaggle_notebook_versions_count.csv
    count >= 10 & vote >= 3
    to #Tmp.csv (53232)

# n_2 (step_n_2.py) collect all the version id

# n_3 (step_n_3.py) collect all the notebooks in all versions 
    # log_download.txt 

    # n_2_1 (step_n_2_1.py) check the notebooks been download
    # log_notebooks_versions.txt
    


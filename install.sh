{
    #
    #  Try to install the environment with the yml file
    #  if env already exists will fail
    #
    conda env create -f environment.yml --name ligmol
} || {
    #
    #  ligmol env does exists, so lets activate it
    #  and install some stuff
    #
    conda activate ligmol
    {
        #
        #  Install via `conda` directly.
        #  This will fail to install all
        #  dependencies. If one fails,
        #  all dependencies will fail to install.
        #
        conda install --yes --file requirements.txt
    } || {
        #
        #  To go around issue above, one can
        #  iterate over all lines in the
        #  requirements.txt file.
        #
        while read requirement; do conda install --yes $requirement; done < requirements.txt
    }
}
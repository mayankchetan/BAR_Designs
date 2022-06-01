
# TURB = 'USC'

# echo "$TURB Running from 3 to 6 m/s for 4 cores"
# sbatch uscArgBasedScript.sh 3 6 4
# sleep 5

# echo "$TURB Running from 7 to 10 m/s for 4 cores"
# sbatch uscArgBasedScript.sh 7 10 4
# sleep 5

# echo "$TURB Running from 11 to 14 m/s for 4 cores"
# sbatch uscArgBasedScript.sh 11 14 4
# sleep 5

# echo "$TURB Running from 15 to 18 m/s for 4 cores"
# sbatch uscArgBasedScript.sh 15 18 4
# sleep 5

# echo "$TURB Running from 19 to 22 m/s for 4 cores"
# sbatch uscArgBasedScript.sh 19 22 4
# sleep 5

# echo "$TURB Running from 23 to 25 m/s for 4 cores"
# sbatch uscArgBasedScript.sh 23 25 4



# TURB = 'URC'

# echo "$TURB Running from 3 to 6 m/s for 4 cores"
# sbatch urcArgBasedScript.sh 3 6 4
# sleep 5

# echo "$TURB Running from 7 to 10 m/s for 4 cores"
# sbatch urcArgBasedScript.sh 7 10 4
# sleep 5

# echo "$TURB Running from 11 to 14 m/s for 4 cores"
# sbatch urcArgBasedScript.sh 11 14 4
# sleep 5

# echo "$TURB Running from 15 to 18 m/s for 4 cores"
# sbatch urcArgBasedScript.sh 15 18 4
# sleep 5

# echo "$TURB Running from 19 to 22 m/s for 4 cores"
# sbatch urcArgBasedScript.sh 19 22 4
# sleep 5

# echo "$TURB Running from 23 to 25 m/s for 4 cores"
# sbatch urcArgBasedScript.sh 23 25 4
# sleep 5



TURB = 'DRC'

echo "$TURB Running from 3 to 6 m/s for 4 cores"
sbatch drcArgBasedScript.sh 3 6 4
sleep 5

echo "$TURB Running from 7 to 10 m/s for 4 cores"
sbatch drcArgBasedScript.sh 7 10 4
sleep 5

echo "$TURB Running from 11 to 14 m/s for 4 cores"
sbatch drcArgBasedScript.sh 11 14 4
sleep 5

echo "$TURB Running from 15 to 18 m/s for 4 cores"
sbatch drcArgBasedScript.sh 15 18 4
sleep 5

echo "$TURB Running from 19 to 22 m/s for 4 cores"
sbatch drcArgBasedScript.sh 19 22 4
sleep 5

echo "$TURB Running from 23 to 25 m/s for 4 cores"
sbatch drcArgBasedScript.sh 23 25 4
sleep 5

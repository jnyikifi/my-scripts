# DSTDIR=/run/media/jny[21~/Lin-backup/x200s-backup
DSTDIR=$1
DATE=`date +%Y-%m-%d`

# pacman -Q > ${DSTDIR}/pkg-${DATE}.list
dpkg-query -l > "${DSTDIR}/pkg-${DATE}.list"
cd /home
tar czp \
    --exclude-backups \
    --exclude-from=/home/jny/Src/misc-scripts/backup-exclude.list \
    -f "${DSTDIR}/jny-${DATE}.tar.gz" jny/

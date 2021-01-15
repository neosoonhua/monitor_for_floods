repeat{
	for (i in 1:562) { #I tried up to 600 and there seems to be no more photo after 562.
		download.file(paste("http://pub.cloudapp.net/CCTVS/", i, sep=""), method="curl", destfile=paste("Test/images/", i, ".jpeg", sep=""))
	}
	print("Downloaded CCTV images at about:")
	print(Sys.time()) #"+08" at the end of the printed string is the timezone.
	Sys.sleep(298) #Wait for 300 seconds. "http://pub.cloudapp.net/CCTVS/" updates the
	# CCTV images every 5 minutes. My machine takes about 2 seconds to run these code.
}